#!/usr/bin/env python3
"""Structural QA for a supplied final Galois 1897 English reader PDF.

This program does not build the reader and does not perform visual inspection.  It
derives the page count from the supplied PDF, cross-checks independent Poppler
tools, and writes an evidence report whose assertions are suitable for release
gating.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import unicodedata
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse

from pypdf import PdfReader
from pypdf.generic import ContentStream


EXPECTED_METADATA = {
    "/Author": "Évariste Galois; Manuscript Typesetting Project; OpenAI GPT-5.6 Sol",
    "/Title": "Évariste Galois — Mathematical Works (1897): Modern English Reader with GPT Critical Notes",
    "/Subject": "Modern-English translation aligned to the audited 1897 French diplomatic transcription",
    "/Creator": "LaTeX with hyperref",
    "/Keywords": "Évariste Galois, English translation, Galois theory, critical edition",
}
EXPECTED_OUTLINE = [
    "Reader contents",
    "1897 publication matter",
    "Picard: Introduction",
    "Periodic continued fractions",
    "Notes on analysis",
    "Algebraic solution of equations",
    "Numerical equations",
    "Theory of numbers",
    "Letter to Auguste Chevalier",
    "Solvability by radicals",
    "Primitive equations",
    "Historical contents and colophon",
]
EXPECTED_OUTLINE_DEPTHS = [0] + [1] * (len(EXPECTED_OUTLINE) - 1)
DEFAULT_REQUIRED_DOIS = [
    "10.5281/zenodo.21924301",
    "10.5281/zenodo.21924302",
    "10.5281/zenodo.21923856",
]
PDFINFO_METADATA_LABELS = {
    "/Author": "Author",
    "/Title": "Title",
    "/Subject": "Subject",
    "/Creator": "Creator",
    "/Keywords": "Keywords",
    "/Producer": "Producer",
}
BOX_NAMES = ("MediaBox", "CropBox", "BleedBox", "TrimBox", "ArtBox")
MARKING_OPERATORS = {
    "Tj",
    "TJ",
    "'",
    '"',
    "Do",
    "S",
    "s",
    "f",
    "F",
    "f*",
    "B",
    "B*",
    "b",
    "b*",
    "sh",
    "INLINE IMAGE",
}
WARNING_RE = re.compile(
    r"(?i)(^\s*(?:LaTeX|Package|Class|pdfTeX)\b[^\r\n]*\bWarning(?:\s*:|\s*\([^)]*\))|"
    r"overfull\s+\\[hv]box|underfull\s+\\[hv]box|"
    r"missing character:|undefined (?:references|citations)|"
    r"rerun (?:to get|LaTeX)|destination with the same identifier)"
)
ERROR_RE = re.compile(
    r"(?i)(^\s*!|Emergency stop|Fatal error|Undefined control sequence|"
    r"No pages of output|TeX capacity exceeded|^\s*LaTeX Error:)"
)
BUILD_OUTPUT_RE = re.compile(
    r"Output written on .*?\((\d+)\s+pages?,\s*(\d+)\s+bytes?\)\.",
    flags=re.IGNORECASE,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def normalized(value: object) -> str:
    return unicodedata.normalize("NFC", str(value)).strip()


def unique(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(values))


def resolve_blank_page_spec(spec: str, page_count: int) -> list[int]:
    """Resolve comma-separated absolute pages and last[-N] selectors."""

    if spec.strip().lower() == "none":
        return []
    pages: list[int] = []
    for raw_token in spec.split(","):
        token = raw_token.strip().lower()
        if not token:
            raise ValueError("empty selector in --expected-blank-pages")
        if token == "last":
            page = page_count
        else:
            match = re.fullmatch(r"last-(\d+)", token)
            if match:
                page = page_count - int(match.group(1))
            elif token.isdecimal():
                page = int(token)
            else:
                raise ValueError(
                    f"invalid blank-page selector {raw_token!r}; use N, last, last-N, or none"
                )
        if not 1 <= page <= page_count:
            raise ValueError(
                f"blank-page selector {raw_token!r} resolves to {page}, outside 1..{page_count}"
            )
        pages.append(page)
    if len(pages) != len(set(pages)):
        raise ValueError("--expected-blank-pages resolves to duplicate page numbers")
    return sorted(pages)


def run_tool(executable: str, arguments: list[str]) -> dict[str, Any]:
    resolved = None
    if os.name == "nt" and not Path(executable).suffix:
        # Prefer a real executable over a same-named batch wrapper.  The Codex
        # runtime can place wrappers earlier on PATH than the Poppler binary.
        resolved = shutil.which(f"{executable}.exe")
    if resolved is None:
        resolved = shutil.which(executable)
    if resolved is None and Path(executable).is_file():
        resolved = str(Path(executable).resolve())
    if resolved is None:
        return {
            "available": False,
            "command": [executable, *arguments],
            "returncode": None,
            "stdout": "",
            "stderr": f"executable not found: {executable}",
        }
    command = [resolved, *arguments]
    try:
        completed = subprocess.run(
            command,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=180,
        )
        return {
            "available": True,
            "command": command,
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "available": True,
            "command": command,
            "returncode": None,
            "stdout": "",
            "stderr": f"{type(exc).__name__}: {exc}",
        }


def public_tool_result(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "available": result["available"],
        "command": result["command"],
        "returncode": result["returncode"],
        "stderr_lines": result["stderr"].splitlines(),
    }


def parse_pdfinfo(text: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        parsed[key.strip()] = value.strip()
    return parsed


def parse_box(text: str | None) -> list[float] | None:
    if not text:
        return None
    values = re.findall(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)", text)
    if len(values) < 4:
        return None
    return [float(value) for value in values[:4]]


def parse_pdffonts(text: str) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    unparsed: list[str] = []
    after_rule = False
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if set(stripped) <= {"-", " "} and "-" in stripped:
            after_rule = True
            continue
        if not after_rule:
            continue
        tokens = stripped.split()
        if len(tokens) < 7 or tokens[-5] not in {"yes", "no"}:
            unparsed.append(line)
            continue
        rows.append(
            {
                "name": tokens[0],
                "description": " ".join(tokens[1:-5]),
                "embedded": tokens[-5] == "yes",
                "subset": tokens[-4] == "yes",
                "unicode_map": tokens[-3] == "yes",
                "object_id": [tokens[-2], tokens[-1]],
            }
        )
    return rows, unparsed


def flatten_outline(reader: PdfReader) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def visit(items: list[object], depth: int) -> None:
        for item in items:
            if isinstance(item, list):
                visit(item, depth + 1)
                continue
            title = getattr(item, "title", None)
            if not title:
                continue
            page: int | None
            error: str | None = None
            try:
                page_index = reader.get_destination_page_number(item)
                page = None if page_index is None else page_index + 1
            except Exception as exc:  # pypdf uses several destination object types
                page = None
                error = f"{type(exc).__name__}: {exc}"
            rows.append(
                {
                    "title": str(title),
                    "depth": depth,
                    "page": page,
                    "error": error,
                }
            )

    visit(reader.outline, 0)
    return rows


def indirect_key(value: object) -> tuple[int, int] | None:
    idnum = getattr(value, "idnum", None)
    generation = getattr(value, "generation", None)
    if idnum is None or generation is None:
        return None
    return int(idnum), int(generation)


def raw_destination_page(
    destination: object,
    named_destinations: dict[str, object],
    page_references: dict[tuple[int, int], int],
) -> tuple[int | None, str | None]:
    if isinstance(destination, str):
        named = named_destinations.get(destination) or named_destinations.get(
            destination.lstrip("/")
        )
        if named is None:
            return None, f"unknown named destination {destination!r}"
        raw_page = getattr(named, "page", None)
        key = indirect_key(raw_page)
        if key in page_references:
            return page_references[key], None
        return None, f"named destination {destination!r} has an unresolved page"

    try:
        resolved = destination.get_object()  # type: ignore[attr-defined]
    except AttributeError:
        resolved = destination
    if isinstance(resolved, (list, tuple)) and resolved:
        key = indirect_key(resolved[0])
        if key in page_references:
            return page_references[key], None
        return None, "destination array does not reference a page in this PDF"
    return None, "unsupported or empty destination"


def inspect_links(reader: PdfReader) -> list[dict[str, Any]]:
    page_references: dict[tuple[int, int], int] = {}
    for number, page in enumerate(reader.pages, start=1):
        key = indirect_key(getattr(page, "indirect_reference", None))
        if key is not None:
            page_references[key] = number

    named_destinations = reader.named_destinations
    rows: list[dict[str, Any]] = []
    for number, page in enumerate(reader.pages, start=1):
        crop = [float(value) for value in page.cropbox]
        crop_left, crop_bottom, crop_right, crop_top = crop
        for reference in page.get("/Annots") or []:
            annotation = reference.get_object()
            if str(annotation.get("/Subtype")) != "/Link":
                continue
            errors: list[str] = []
            rect_value = annotation.get("/Rect")
            try:
                rect = [float(value) for value in rect_value]
            except (TypeError, ValueError):
                rect = []
            if len(rect) != 4 or not all(math.isfinite(value) for value in rect):
                errors.append("missing or invalid /Rect")
            else:
                left, right = sorted((rect[0], rect[2]))
                bottom, top = sorted((rect[1], rect[3]))
                tolerance = 0.5
                if (
                    left < crop_left - tolerance
                    or bottom < crop_bottom - tolerance
                    or right > crop_right + tolerance
                    or top > crop_top + tolerance
                ):
                    errors.append("/Rect lies outside the page CropBox")

            kind: str | None = None
            target: str | int | None = None
            if annotation.get("/Dest") is not None:
                kind = "GoTo"
                target, error = raw_destination_page(
                    annotation.get("/Dest"), named_destinations, page_references
                )
                if error:
                    errors.append(error)
            elif annotation.get("/A") is not None:
                action = annotation.get("/A").get_object()
                action_kind = str(action.get("/S"))
                kind = action_kind.lstrip("/")
                if action_kind == "/URI":
                    uri = str(action.get("/URI") or "").strip()
                    target = uri
                    parsed = urlparse(uri)
                    if parsed.scheme in {"http", "https"}:
                        if not parsed.netloc or any(character.isspace() for character in uri):
                            errors.append("malformed HTTP(S) URI")
                    elif parsed.scheme == "mailto":
                        if not parsed.path:
                            errors.append("malformed mailto URI")
                    else:
                        errors.append(f"unsupported or missing URI scheme: {parsed.scheme!r}")
                elif action_kind == "/GoTo":
                    target, error = raw_destination_page(
                        action.get("/D"), named_destinations, page_references
                    )
                    if error:
                        errors.append(error)
                else:
                    errors.append(f"unsupported link action {action_kind!r}")
            else:
                errors.append("link has neither /Dest nor /A")

            rows.append(
                {
                    "source_page": number,
                    "rect": rect,
                    "kind": kind,
                    "target": target,
                    "errors": errors,
                }
            )
    return rows


def page_box_values(page: object, name: str) -> list[float]:
    attribute = name.lower()
    return [float(value) for value in getattr(page, attribute)]


def valid_box(box: list[float]) -> bool:
    return (
        len(box) == 4
        and all(math.isfinite(value) for value in box)
        and box[2] > box[0]
        and box[3] > box[1]
    )


def box_inside(inner: list[float], outer: list[float], tolerance: float = 0.01) -> bool:
    return (
        inner[0] >= outer[0] - tolerance
        and inner[1] >= outer[1] - tolerance
        and inner[2] <= outer[2] + tolerance
        and inner[3] <= outer[3] + tolerance
    )


def marking_operators(page: object, reader: PdfReader) -> tuple[list[str], int, str | None]:
    contents = page.get_contents()  # type: ignore[attr-defined]
    if contents is None:
        return [], 0, None
    try:
        content_bytes = contents.get_data()
        stream = ContentStream(contents, reader)
        operators = []
        for _operands, operator in stream.operations:
            name = operator.decode("latin-1") if isinstance(operator, bytes) else str(operator)
            if name in MARKING_OPERATORS:
                operators.append(name)
        return sorted(set(operators)), len(content_bytes), None
    except Exception as exc:
        return [], 0, f"{type(exc).__name__}: {exc}"


def scan_build_logs(
    paths: list[Path], allowed_warning_patterns: list[re.Pattern[str]]
) -> dict[str, Any]:
    logs: list[dict[str, Any]] = []
    all_errors: list[dict[str, Any]] = []
    all_warnings: list[dict[str, Any]] = []
    unreadable: list[str] = []
    for supplied_path in paths:
        path = supplied_path.resolve()
        if not path.is_file():
            unreadable.append(str(path))
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        unwrapped_text = text.replace("\r", "").replace("\n", "")
        output_receipts = [
            {"page_count": int(page_count), "bytes": int(byte_count)}
            for page_count, byte_count in BUILD_OUTPUT_RE.findall(unwrapped_text)
        ]
        errors: list[dict[str, Any]] = []
        warnings: list[dict[str, Any]] = []
        allowed: list[dict[str, Any]] = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            entry = {"line": line_number, "text": line.rstrip()}
            if ERROR_RE.search(line):
                errors.append(entry)
                all_errors.append({"log": str(path), **entry})
            elif WARNING_RE.search(line):
                if any(pattern.search(line) for pattern in allowed_warning_patterns):
                    allowed.append(entry)
                else:
                    warnings.append(entry)
                    all_warnings.append({"log": str(path), **entry})
        logs.append(
            {
                "path": str(path),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "output_receipts": output_receipts,
                "errors": errors,
                "unapproved_warnings": warnings,
                "allowed_warnings": allowed,
            }
        )
    return {
        "logs": logs,
        "unreadable": unreadable,
        "errors": all_errors,
        "unapproved_warnings": all_warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run structural (not visual) release QA on a final English reader PDF."
    )
    parser.add_argument("pdf", type=Path, help="final reader PDF to inspect")
    parser.add_argument("output", type=Path, help="JSON report to write")
    parser.add_argument(
        "--expected-blank-pages",
        required=True,
        metavar="SPEC",
        help="comma-separated N, last, or last-N selectors; use 'none' for no blanks",
    )
    parser.add_argument(
        "--build-log",
        action="append",
        required=True,
        type=Path,
        help="final TeX/build log to scan; repeat for multiple logs",
    )
    parser.add_argument(
        "--allow-log-warning-regex",
        action="append",
        default=[],
        metavar="REGEX",
        help="explicitly allow matching build-log warning lines; repeat as needed",
    )
    parser.add_argument(
        "--required-doi",
        action="append",
        default=[],
        help="additional DOI string that both extractors must recover",
    )
    parser.add_argument("--pdfinfo-command", default="pdfinfo")
    parser.add_argument("--pdffonts-command", default="pdffonts")
    parser.add_argument("--pdftotext-command", default="pdftotext")
    args = parser.parse_args()

    pdf = args.pdf.resolve()
    output = args.output.resolve()
    if not pdf.is_file():
        parser.error(f"PDF does not exist: {pdf}")
    if output.suffix.lower() != ".json":
        parser.error("output path must end in .json")
    if output == pdf:
        parser.error("output JSON must not overwrite the input PDF")
    try:
        allowed_warning_patterns = [
            re.compile(pattern) for pattern in args.allow_log_warning_regex
        ]
    except re.error as exc:
        parser.error(f"invalid --allow-log-warning-regex: {exc}")

    try:
        reader = PdfReader(str(pdf), strict=True)
    except Exception as exc:
        parser.error(f"strict PDF parse failed: {type(exc).__name__}: {exc}")
    if reader.is_encrypted:
        try:
            decryption_result = reader.decrypt("")
        except Exception as exc:
            parser.error(f"encrypted PDF could not be inspected: {type(exc).__name__}: {exc}")
        if not decryption_result:
            parser.error("encrypted PDF requires a password; release readers must be unencrypted")
    page_count = len(reader.pages)
    try:
        expected_blank_pages = resolve_blank_page_spec(
            args.expected_blank_pages, page_count
        )
    except ValueError as exc:
        parser.error(str(exc))

    metadata = {
        str(key): normalized(value) for key, value in (reader.metadata or {}).items()
    }
    try:
        outline = flatten_outline(reader)
        outline_read_error: str | None = None
    except Exception as exc:
        outline = []
        outline_read_error = f"{type(exc).__name__}: {exc}"
    try:
        links = inspect_links(reader)
        link_read_error: str | None = None
    except Exception as exc:
        links = []
        link_read_error = f"{type(exc).__name__}: {exc}"
    required_dois = unique([*DEFAULT_REQUIRED_DOIS, *args.required_doi])

    text_lengths: list[int] = []
    extracted: list[str] = []
    extraction_errors: list[dict[str, Any]] = []
    page_rows: list[dict[str, Any]] = []
    structural_blank_pages: list[int] = []
    page_boxes_by_name: dict[str, list[list[float]]] = {
        name: [] for name in BOX_NAMES
    }
    direct_font_names: set[str] = set()

    for number, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as exc:
            text = ""
            extraction_errors.append(
                {"page": number, "error": f"{type(exc).__name__}: {exc}"}
            )
        extracted.append(text)
        text_lengths.append(len(text.strip()))

        operators, content_length, content_error = marking_operators(page, reader)
        if not operators and content_error is None:
            structural_blank_pages.append(number)

        boxes = {name: page_box_values(page, name) for name in BOX_NAMES}
        for name, box in boxes.items():
            page_boxes_by_name[name].append(box)

        resources = page.get("/Resources")
        if resources:
            fonts = resources.get_object().get("/Font")
            if fonts:
                for reference in fonts.get_object().values():
                    name = reference.get_object().get("/BaseFont")
                    if name:
                        direct_font_names.add(str(name))

        page_rows.append(
            {
                "page": number,
                "text_characters": len(text.strip()),
                "content_stream_bytes": content_length,
                "marking_operators": operators,
                "content_parse_error": content_error,
                "boxes": boxes,
            }
        )

    pypdf_text = "\n".join(extracted)
    pdfinfo_result = run_tool(args.pdfinfo_command, ["-box", str(pdf)])
    pdffonts_result = run_tool(args.pdffonts_command, [str(pdf)])
    pdftotext_result = run_tool(
        args.pdftotext_command, ["-enc", "UTF-8", str(pdf), "-"]
    )
    pdfinfo = parse_pdfinfo(pdfinfo_result["stdout"])
    pdffonts_rows, pdffonts_unparsed = parse_pdffonts(pdffonts_result["stdout"])

    pdftotext_pages = pdftotext_result["stdout"].split("\f")
    if pdftotext_pages and not pdftotext_pages[-1].strip():
        pdftotext_pages.pop()
    pdftotext_text = "\n".join(pdftotext_pages)

    log_report = scan_build_logs(args.build_log, allowed_warning_patterns)
    build_receipts: list[dict[str, Any]] = []
    for log in log_report["logs"]:
        for receipt in log["output_receipts"]:
            receipt["matches_pdf_page_count"] = receipt["page_count"] == page_count
            receipt["matches_pdf_bytes"] = receipt["bytes"] == pdf.stat().st_size
            build_receipts.append(receipt)

    page_box_errors: list[dict[str, Any]] = []
    for row in page_rows:
        boxes = row["boxes"]
        for name, box in boxes.items():
            if not valid_box(box):
                page_box_errors.append(
                    {"page": row["page"], "box": name, "reason": "invalid coordinates"}
                )
        media = boxes["MediaBox"]
        for name in BOX_NAMES[1:]:
            if not box_inside(boxes[name], media):
                page_box_errors.append(
                    {
                        "page": row["page"],
                        "box": name,
                        "reason": "not contained by MediaBox",
                    }
                )

    unique_page_boxes = {
        name: [list(values) for values in sorted({tuple(box) for box in boxes})]
        for name, boxes in page_boxes_by_name.items()
    }

    pdfinfo_pages = pdfinfo.get("Pages", "")
    pdfinfo_file_size_match = re.search(r"\d+", pdfinfo.get("File size", ""))
    pdfinfo_metadata_matches = all(
        normalized(pdfinfo.get(label, "")) == metadata.get(key, "")
        for key, label in PDFINFO_METADATA_LABELS.items()
    )
    pdfinfo_boxes_match = True
    if page_rows:
        first_page_boxes = page_rows[0]["boxes"]
        for name in BOX_NAMES:
            reported_box = parse_box(pdfinfo.get(name))
            if reported_box is None or any(
                abs(left - right) > 0.02
                for left, right in zip(reported_box, first_page_boxes[name])
            ):
                pdfinfo_boxes_match = False
                break

    doi_matrix = {
        doi: {
            "pypdf": doi in pypdf_text,
            "pdftotext": doi in pdftotext_text,
        }
        for doi in required_dois
    }
    assertions = {
        "page_count_derived_and_positive": page_count > 0,
        "not_encrypted": not reader.is_encrypted,
        "pdfinfo_available": pdfinfo_result["available"],
        "pdfinfo_succeeded": pdfinfo_result["returncode"] == 0,
        "pdfinfo_no_diagnostics": not pdfinfo_result["stderr"].strip(),
        "pdfinfo_page_count_matches_pdf": pdfinfo_pages.isdecimal()
        and int(pdfinfo_pages) == page_count,
        "pdfinfo_encryption_matches_pdf": pdfinfo.get("Encrypted", "")
        .lower()
        .startswith("no"),
        "pdfinfo_file_size_matches_pdf": pdfinfo_file_size_match is not None
        and int(pdfinfo_file_size_match.group(0)) == pdf.stat().st_size,
        "pdfinfo_metadata_matches_pdf": pdfinfo_metadata_matches,
        "pdfinfo_page_boxes_match_first_page": pdfinfo_boxes_match,
        "required_metadata_exact": all(
            metadata.get(key) == normalized(value)
            for key, value in EXPECTED_METADATA.items()
        ),
        "outline_titles_exact_and_ordered": [row["title"] for row in outline]
        == EXPECTED_OUTLINE,
        "outline_hierarchy_exact": [row["depth"] for row in outline]
        == EXPECTED_OUTLINE_DEPTHS,
        "outline_tree_readable": outline_read_error is None,
        "all_outline_destinations_resolve": bool(outline)
        and all(
            row["error"] is None
            and isinstance(row["page"], int)
            and 1 <= row["page"] <= page_count
            for row in outline
        ),
        "outline_destinations_follow_document_order": bool(outline)
        and [row["page"] for row in outline]
        == sorted({row["page"] for row in outline if isinstance(row["page"], int)}),
        "link_annotations_present": bool(links),
        "link_annotations_readable": link_read_error is None,
        "all_link_annotations_valid": bool(links)
        and all(not row["errors"] for row in links),
        "all_page_content_streams_parse": all(
            row["content_parse_error"] is None for row in page_rows
        ),
        "all_page_boxes_valid_and_nested": not page_box_errors,
        "single_media_and_crop_geometry": len(unique_page_boxes["MediaBox"]) == 1
        and len(unique_page_boxes["CropBox"]) == 1,
        "blank_topology_matches_declared": structural_blank_pages
        == expected_blank_pages,
        "pypdf_extraction_succeeded_on_all_pages": not extraction_errors,
        "pypdf_extractable_text_nonempty": bool(pypdf_text.strip()),
        "pdftotext_available": pdftotext_result["available"],
        "pdftotext_succeeded": pdftotext_result["returncode"] == 0,
        "pdftotext_no_diagnostics": not pdftotext_result["stderr"].strip(),
        "pdftotext_page_count_matches_pdf": len(pdftotext_pages) == page_count,
        "pdftotext_extractable_text_nonempty": bool(pdftotext_text.strip()),
        "all_required_dois_extract_with_pypdf": all(
            row["pypdf"] for row in doi_matrix.values()
        ),
        "all_required_dois_extract_with_pdftotext": all(
            row["pdftotext"] for row in doi_matrix.values()
        ),
        "pdffonts_available": pdffonts_result["available"],
        "pdffonts_succeeded": pdffonts_result["returncode"] == 0,
        "pdffonts_no_diagnostics": not pdffonts_result["stderr"].strip(),
        "font_rows_present_and_parseable": bool(pdffonts_rows)
        and not pdffonts_unparsed,
        "all_fonts_embedded": bool(pdffonts_rows)
        and all(row["embedded"] for row in pdffonts_rows),
        "direct_font_resources_present": bool(direct_font_names),
        "build_logs_readable": bool(args.build_log) and not log_report["unreadable"],
        "build_logs_nonempty": bool(log_report["logs"])
        and all(log["bytes"] > 0 for log in log_report["logs"]),
        "build_log_output_receipts_present": bool(log_report["logs"])
        and all(log["output_receipts"] for log in log_report["logs"]),
        "all_build_receipt_page_counts_match_pdf": bool(build_receipts)
        and all(receipt["matches_pdf_page_count"] for receipt in build_receipts),
        "a_build_receipt_matches_pdf_page_count_and_bytes": any(
            receipt["matches_pdf_page_count"] and receipt["matches_pdf_bytes"]
            for receipt in build_receipts
        ),
        "build_logs_have_no_errors": not log_report["errors"],
        "build_logs_have_no_unapproved_warnings": not log_report[
            "unapproved_warnings"
        ],
    }
    report = {
        "schema_version": 2,
        "assessment_scope": "structural-and-mechanical; no visual inspection performed",
        "pdf": str(pdf),
        "bytes": pdf.stat().st_size,
        "sha256": sha256(pdf),
        "page_count": page_count,
        "metadata": {
            "actual": metadata,
            "required_exact": EXPECTED_METADATA,
        },
        "pdfinfo": {
            "tool": public_tool_result(pdfinfo_result),
            "fields": pdfinfo,
        },
        "outline": {
            "entries": outline,
            "read_error": outline_read_error,
        },
        "links": {
            "count": len(links),
            "annotations": links,
            "read_error": link_read_error,
        },
        "page_boxes": {
            "unique_effective_boxes": unique_page_boxes,
            "errors": page_box_errors,
        },
        "blank_topology": {
            "selector_spec": args.expected_blank_pages,
            "expected_pages": expected_blank_pages,
            "structurally_blank_pages": structural_blank_pages,
        },
        "extraction": {
            "pypdf_page_text_lengths": text_lengths,
            "pypdf_errors": extraction_errors,
            "pdftotext_tool": public_tool_result(pdftotext_result),
            "pdftotext_page_count": len(pdftotext_pages),
            "pdftotext_page_text_lengths": [
                len(text.strip()) for text in pdftotext_pages
            ],
            "required_doi_strings": doi_matrix,
        },
        "fonts": {
            "direct_resource_names": sorted(direct_font_names),
            "pdffonts_tool": public_tool_result(pdffonts_result),
            "rows": pdffonts_rows,
            "unparsed_rows": pdffonts_unparsed,
            "not_embedded": [
                row["name"] for row in pdffonts_rows if not row["embedded"]
            ],
        },
        "build_logs": {
            "allowed_warning_regexes": args.allow_log_warning_regex,
            **log_report,
        },
        "pages": page_rows,
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
                "sha256": report["sha256"],
                "failed_assertions": [
                    name for name, passed in assertions.items() if not passed
                ],
            },
            indent=2,
        )
    )
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
