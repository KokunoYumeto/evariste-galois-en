#!/usr/bin/env python3
"""Mechanical raster QA for a rendered Galois 1897 English reader.

The expected page count and blank topology come from a current structural-QA
report.  Pixel statistics can detect missing pages and gross raster surprises,
but they are not visual inspection and this script never records them as such.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat


VISUAL_INSPECTION_TEMPLATE = (
    Path(__file__).resolve().parent
    / "galois-en-publication"
    / "qa"
    / "galois_english_pdf_visual_inspection.template.json"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def page_number(path: Path) -> int:
    match = re.fullmatch(r"page-(\d+)", path.stem, flags=re.IGNORECASE)
    if not match:
        raise ValueError(f"render filename does not match page-N.png: {path.name}")
    return int(match.group(1))


def metrics(path: Path, dark_threshold: int, edge_width: int) -> dict[str, Any]:
    with Image.open(path) as image:
        gray = image.convert("L")
        stats = ImageStat.Stat(gray)
        histogram = gray.histogram()
        dark_pixel_count = sum(histogram[:dark_threshold])
        pixel_count = gray.width * gray.height
        dark = gray.point(lambda value: 255 if value < dark_threshold else 0)
        bbox = dark.getbbox()

        strips = [
            gray.crop((0, 0, gray.width, edge_width)),
            gray.crop((0, gray.height - edge_width, gray.width, gray.height)),
            gray.crop((0, 0, edge_width, gray.height)),
            gray.crop((gray.width - edge_width, 0, gray.width, gray.height)),
        ]
        edge_dark_pixel_count = sum(
            sum(strip.histogram()[:dark_threshold]) for strip in strips
        )
        dpi_value = image.info.get("dpi")
        if isinstance(dpi_value, tuple):
            dpi = [round(float(value), 4) for value in dpi_value[:2]]
        else:
            dpi = None

        return {
            "file": path.name,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "size": [gray.width, gray.height],
            "dpi_metadata": dpi,
            "mean": round(stats.mean[0], 4),
            "stddev": round(stats.stddev[0], 4),
            "content_bbox_at_threshold": list(bbox) if bbox else None,
            "dark_threshold": dark_threshold,
            "dark_pixel_count": dark_pixel_count,
            "dark_pixel_fraction": round(dark_pixel_count / pixel_count, 10),
            "edge_width_pixels": edge_width,
            "edge_dark_pixel_count": edge_dark_pixel_count,
            "mechanically_blank": dark_pixel_count == 0,
            "mechanically_black": stats.mean[0] < 5,
            "dark_pixels_touch_edge": edge_dark_pixel_count > 0,
        }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run pixel-metric QA; this does not perform visual inspection."
    )
    parser.add_argument("render_directory", type=Path)
    parser.add_argument("structural_report", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--dark-threshold",
        type=int,
        default=245,
        help="grayscale values below this threshold count as marked pixels",
    )
    parser.add_argument(
        "--edge-width",
        type=int,
        default=2,
        help="border width in pixels used for edge-contact detection",
    )
    args = parser.parse_args()

    if not 1 <= args.dark_threshold <= 255:
        parser.error("--dark-threshold must be in 1..255")
    if args.edge_width < 1:
        parser.error("--edge-width must be positive")

    render_directory = args.render_directory.resolve()
    structural_report_path = args.structural_report.resolve()
    output = args.output.resolve()
    if not render_directory.is_dir():
        parser.error(f"render directory does not exist: {render_directory}")
    if not structural_report_path.is_file():
        parser.error(f"structural report does not exist: {structural_report_path}")
    if output.suffix.lower() != ".json":
        parser.error("output path must end in .json")
    if output == structural_report_path:
        parser.error("output JSON must not overwrite the structural report")

    structural = json.loads(structural_report_path.read_text(encoding="utf-8"))
    structural_schema_supported = structural.get("schema_version") == 2
    page_count = structural.get("page_count")
    expected_blank_pages = (
        structural.get("blank_topology", {}).get("expected_pages")
    )
    if not isinstance(page_count, int) or page_count < 1:
        parser.error("structural report has no positive integer page_count")
    if (
        not isinstance(expected_blank_pages, list)
        or not all(isinstance(page, int) for page in expected_blank_pages)
        or expected_blank_pages != sorted(set(expected_blank_pages))
        or any(page < 1 or page > page_count for page in expected_blank_pages)
    ):
        parser.error("structural report has invalid blank_topology.expected_pages")

    paths = sorted(render_directory.glob("page-*.png"), key=page_number)
    numbers = [page_number(path) for path in paths]
    rows: list[dict[str, Any]] = []
    mechanically_blank_pages: list[int] = []
    black_pages: list[int] = []
    edge_contacts: list[int] = []
    for path in paths:
        number = page_number(path)
        row = metrics(path, args.dark_threshold, args.edge_width)
        row["page"] = number
        rows.append(row)
        if row["mechanically_blank"]:
            mechanically_blank_pages.append(number)
        if row["mechanically_black"]:
            black_pages.append(number)
        if row["dark_pixels_touch_edge"]:
            edge_contacts.append(number)

    expected_numbers = list(range(1, page_count + 1))
    assertions = {
        "structural_report_schema_supported": structural_schema_supported,
        "structural_report_passed": structural.get("result") == "PASS",
        "rendered_page_count_matches_structural_report": len(paths) == page_count,
        "rendered_page_numbers_are_exact_and_contiguous": numbers
        == expected_numbers,
        "mechanical_blank_topology_matches_structural_report": mechanically_blank_pages
        == expected_blank_pages,
        "no_mechanically_black_pages": not black_pages,
        "no_dark_pixel_edge_contacts": not edge_contacts,
        "single_render_geometry": bool(rows)
        and len({tuple(row["size"]) for row in rows}) == 1,
    }
    contact_sheets = sorted((render_directory / "contacts").glob("contact-*.png"))
    report = {
        "schema_version": 2,
        "assessment_scope": "mechanical raster metrics only; no visual inspection performed",
        "render_directory": str(render_directory),
        "structural_report": {
            "path": str(structural_report_path),
            "sha256": sha256(structural_report_path),
            "pdf": structural.get("pdf"),
            "pdf_sha256": structural.get("sha256"),
            "page_count": page_count,
            "blank_pages": expected_blank_pages,
            "result": structural.get("result"),
        },
        "metric_parameters": {
            "dark_threshold": args.dark_threshold,
            "edge_width_pixels": args.edge_width,
            "render_dpi": sorted(
                {
                    tuple(row["dpi_metadata"])
                    for row in rows
                    if row["dpi_metadata"] is not None
                }
            ),
        },
        "page_metrics": rows,
        "mechanically_blank_pages": mechanically_blank_pages,
        "mechanically_black_pages": black_pages,
        "dark_edge_contact_pages": edge_contacts,
        "contact_sheet_files_present_but_not_inspected": [
            str(path.resolve()) for path in contact_sheets
        ],
        "visual_inspection": {
            "status": "NOT_PERFORMED_BY_THIS_SCRIPT",
            "template": str(VISUAL_INSPECTION_TEMPLATE),
            "template_sha256": sha256(VISUAL_INSPECTION_TEMPLATE)
            if VISUAL_INSPECTION_TEMPLATE.is_file()
            else None,
        },
        "assertions": assertions,
        "result": "PASS" if all(assertions.values()) else "FAIL",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "result": report["result"],
                "page_count": page_count,
                "failed_assertions": [
                    name for name, passed in assertions.items() if not passed
                ],
                "visual_inspection": "NOT_PERFORMED",
            },
            indent=2,
        )
    )
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
