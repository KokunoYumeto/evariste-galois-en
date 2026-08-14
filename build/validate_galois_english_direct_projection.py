#!/usr/bin/env python3
"""Validate the source-faithful projection of the Galois English corpus.

The direct reader deliberately reuses the exact eleven translated work bodies.
Only its driver and wrappers may change how modern critical apparatus renders.
This validator therefore treats byte equality of the work bodies as the primary
source invariant and, when a PDF is supplied, proves that the resulting reader
has the expected navigation/topology and no rendered modern apparatus.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath
from typing import Iterable

from pypdf import PdfReader


EXPECTED_COMPONENTS = tuple(f"W{number:02d}" for number in range(1, 12))
EXPECTED_SEGMENTS = 587
EXPECTED_DIRECT_PAGES = 81
EXPECTED_DIRECT_BLANK_PAGES = (38, 76, 79, 80, 81)
EXPECTED_SOURCE_DESTINATIONS = 73
SOURCE_DESTINATIONS_SHA256 = (
    "05C2D4D506CC9E706E8A74E66DD2C0301838A5DEA071760E8DBCBFD04FF750DF"
)
EXPECTED_WORK_BOOKMARKS = (
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
)
EXPECTED_HISTORICAL_CALLS = {
    "GalHistoricalFootnote": 8,
    "GalHistoricalFootnoteText": 5,
    "GalHistoricalFootnoteMark": 3,
    "GalHistoricalNote": 6,
}
EXPECTED_MODERN_CALLS = {
    "GalCriticalNote": 62,
    "GalWitnessNote": 3,
    "GalPrintedError": 17,
    "GalPrintedOmission": 1,
    "GalSourceError": 14,
    "GalWitnessVariant": 6,
    "GalSourceErrorMark": 9,
}
WORK_NAMES = (
    "GAL1897_W01_PRELIMS.tex",
    "GAL1897_W02_INTRODUCTION.tex",
    "GAL1897_W03_CONTINUED_FRACTIONS.tex",
    "GAL1897_W04_NOTES_ANALYSIS.tex",
    "GAL1897_W05_ALGEBRAIC_RESOLUTION_ANALYSIS.tex",
    "GAL1897_W06_NUMERICAL_EQUATIONS.tex",
    "GAL1897_W07_NUMBER_THEORY.tex",
    "GAL1897_W08_CHEVALIER_LETTER.tex",
    "GAL1897_W09_RADICALS_MEMOIR.tex",
    "GAL1897_W10_PRIMITIVE_EQUATIONS.tex",
    "GAL1897_W11_BACKMATTER.tex",
)
FIGURE_NAMES = (
    "PDF007_L0006_PUBLISHER_DEVICE.png",
    "PDF019_L0018_PORTRAIT_PLATE.png",
    "PDF021_L0020_PORTRAIT_PLATE_DEGRADED.png",
    "PDF024_L0023_MARGIN_X_ENHANCED.png",
    "PDF029_L0028_END_ORNAMENT_ENHANCED.png",
    "PDF030_L0029_TITLE_MARK_ENHANCED.png",
    "PDF052_L0051_TERMINAL_ORNAMENT_ENHANCED.png",
    "PDF052_L0051_TERMINAL_ORNAMENT_RAW.png",
    "PDF093_L0092_PRINTER_JOB_NUMBER_ENHANCED.png",
)
DIRECT_MASTER = "GAL1897_EN_SOURCE_FAITHFUL_READER.tex"
ANNOTATED_MASTER = "GAL1897_EN_MODERN_READER.tex"
SCRIPT_ROOT = Path(__file__).resolve().parent
FROZEN_AUTHORITY_PATH = SCRIPT_ROOT / "GALOIS_R3_FROZEN_AUTHORITY.json"
CONCEPT_DOI = "10.5281/zenodo.21924301"
FRENCH_CONCEPT_DOI = "10.5281/zenodo.21923856"
ANNOTATED_PREDECESSOR_DOI = "10.5281/zenodo.21926209"
ZENODO_DOI_RE = re.compile(r"10\.5281/zenodo\.\d+")
SEGMENT_RE = re.compile(r"(?m)^\s*%\s*ENSEG:(W\d{2}):PDF(\d{3}):(\d{4})\s*$")
STABLE_ID_RE = re.compile(
    r"(?:POST-P13-A\d{3}|W\d{2}-(?:PE|SE|WV|DA|U|NA|TERM)\d{3})"
)
FORBIDDEN_RENDERED_PATTERNS = (
    ("editorial_reference", re.compile(r"Editorial\s+reference\s*:", re.I)),
    ("gpt_critical_note", re.compile(r"GPT\s+Critical\s+Note", re.I)),
    ("stable_internal_id", STABLE_ID_RE),
    ("visible_source_label", re.compile(r"Source\s+PDF\s*\d", re.I)),
    ("dagger_glyph", re.compile(r"[†‡]")),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def sha256_lines(values: Iterable[str]) -> str:
    payload = "".join(f"{value}\n" for value in values).encode("utf-8")
    return hashlib.sha256(payload).hexdigest().upper()


def load_frozen_authority() -> dict[str, object]:
    if FROZEN_AUTHORITY_PATH.is_symlink():
        raise ValueError("Frozen authority JSON may not be a symlink")
    raw = FROZEN_AUTHORITY_PATH.resolve(strict=True).read_bytes()
    try:
        authority = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError("Frozen authority is not valid UTF-8 JSON") from error
    if not isinstance(authority, dict) or authority.get("schema_version") != 1:
        raise RuntimeError("Frozen authority schema/version mismatch")
    english = authority.get("english_annotated_predecessor")
    if not isinstance(english, dict) or english.get("exact_doi") != ANNOTATED_PREDECESSOR_DOI:
        raise RuntimeError("Frozen English predecessor identity mismatch")
    works = english.get("work_files")
    figures = english.get("figure_files")
    if not isinstance(works, list) or [item.get("name") for item in works if isinstance(item, dict)] != list(WORK_NAMES):
        raise RuntimeError("Frozen authority has the wrong ordered work-file universe")
    if not isinstance(figures, list) or [item.get("name") for item in figures if isinstance(item, dict)] != list(FIGURE_NAMES):
        raise RuntimeError("Frozen authority has the wrong ordered figure universe")
    for collection in (works, figures):
        for item in collection:
            if (
                not isinstance(item, dict)
                or not isinstance(item.get("bytes"), int)
                or isinstance(item.get("bytes"), bool)
                or item["bytes"] < 0
                or not isinstance(item.get("sha256"), str)
                or not re.fullmatch(r"[0-9A-F]{64}", item["sha256"])
            ):
                raise RuntimeError("Frozen authority contains a malformed file pin")
    return authority


def frozen_file_record(path: Path, record: dict[str, object], root: Path) -> dict[str, object]:
    source = require_file(path, root)
    actual = (source.stat().st_size, sha256(source))
    expected = (int(record["bytes"]), str(record["sha256"]))
    if actual != expected:
        raise RuntimeError(f"Frozen authority file changed: {record['name']}")
    return {"name": record["name"], "bytes": actual[0], "sha256": actual[1]}


def authority_set_sha256(records: Iterable[dict[str, object]]) -> str:
    return sha256_lines(
        f"{record['name']}\t{record['bytes']}\t{record['sha256']}" for record in records
    )


def validate_annotated_master_against_predecessor(
    master_text: str, record: dict[str, object]
) -> dict[str, object]:
    line_pattern = re.compile(
        r"(?m)^[ \t]*\{\\small Exact release DOI:.*?\\par\}[ \t]*$"
    )
    matches = line_pattern.findall(master_text)
    if len(matches) != 1:
        raise RuntimeError("Annotated master must contain exactly one exact-release DOI line")
    normalized_line = ZENODO_DOI_RE.sub(ANNOTATED_PREDECESSOR_DOI, matches[0])
    normalized = line_pattern.sub(lambda _match: normalized_line, master_text, count=1).encode("utf-8")
    actual = (len(normalized), hashlib.sha256(normalized).hexdigest().upper())
    expected = (int(record["bytes"]), str(record["sha256"]))
    if actual != expected:
        raise RuntimeError("Annotated master changed beyond the permitted exact-DOI injection")
    return {
        "name": record["name"],
        "normalized_bytes": actual[0],
        "normalized_sha256": actual[1],
        "normalization": "exact DOI line restored to frozen annotated predecessor",
        "result": "PASS",
    }


def require_exact_doi_universe(text: str, exact_doi: str, role: str, extractor: str) -> list[str]:
    expected = {CONCEPT_DOI, FRENCH_CONCEPT_DOI, exact_doi}
    actual = set(ZENODO_DOI_RE.findall(text))
    if actual != expected:
        raise RuntimeError(
            f"{role} DOI universe changed under {extractor}: actual={sorted(actual)!r}, "
            f"expected={sorted(expected)!r}"
        )
    return sorted(actual)


def require_file(path: Path, root: Path) -> Path:
    if path.is_symlink():
        raise ValueError(f"Symlink source is prohibited: {path}")
    resolved = path.resolve(strict=True)
    if not resolved.is_file():
        raise FileNotFoundError(path)
    try:
        resolved.relative_to(root.resolve(strict=True))
    except ValueError as error:
        raise ValueError(f"Source escapes declared root: {path}") from error
    return resolved


def read_utf8(path: Path, root: Path) -> str:
    return require_file(path, root).read_text(encoding="utf-8")


def macro_call_count(text: str, name: str) -> int:
    return len(re.findall(rf"\\{re.escape(name)}\s*\{{", text))


def strip_tex_comments(text: str) -> str:
    return re.sub(r"(?m)(?<!\\)%.*$", "", text)


def require_master_policy(master: str) -> dict[str, object]:
    compact = re.sub(r"\s+", "", strip_tex_comments(master))
    required = {
        "critical_note_empty": r"\providecommand{\GalCriticalNote}[3]{}",
        "witness_note_empty": r"\providecommand{\GalWitnessNote}[3]{}",
        "editorial_reference_empty": r"\providecommand{\GalEditorialReference}[1]{}",
        "critical_marker_empty": r"\providecommand{\GalCriticalMarker}{}",
        "printed_omission_empty": r"\providecommand{\GalPrintedOmission}[1]{}",
        "source_error_mark_empty": r"\providecommand{\GalSourceErrorMark}[1]{}",
        "proof_gap_mark_empty": r"\providecommand{\GalProofGapMark}[1]{}",
        "printed_error_first_arg": r"\providecommand{\GalPrintedError}[2]{#1}",
        "source_error_first_arg": r"\providecommand{\GalSourceError}[2]{#1}",
        "witness_variant_first_arg": r"\providecommand{\GalWitnessVariant}[2]{#1}",
        "copy_marks_empty": r"\providecommand{\GalCopySpecificMarks}[4]{}",
        "copy_mark_image_empty": r"\providecommand{\GalCopySpecificMarkImage}[4]{}",
        "invisible_source_anchor": r"\providecommand{\GalSourceAnchor}[2]{\hypertarget{source-#1}{}}",
    }
    result: dict[str, object] = {}
    for label, wanted in required.items():
        passed = wanted in compact
        result[label] = passed
        if not passed:
            raise RuntimeError(f"Direct-reader master policy failed: {label}")
    prohibited = {
        "tcolorbox_package": r"\usepackage[most]{tcolorbox}",
        "critical_box_definition": r"\newtcolorbox{GalCriticalBox}",
        "visible_source_label": "SourcePDF#1",
    }
    for label, needle in prohibited.items():
        present = needle in compact
        result[f"{label}_absent"] = not present
        if present:
            raise RuntimeError(f"Direct-reader master still enables {label}")
    return result


def require_wrapper_policy(direct: Path) -> dict[str, object]:
    wrappers = direct / "tex" / "wrappers"
    texts = {
        f"W{number:02d}": read_utf8(wrappers / f"W{number:02d}.tex", direct)
        for number in range(1, 12)
    }
    compact = {
        name: re.sub(r"\s+", "", strip_tex_comments(text)) for name, text in texts.items()
    }
    expected_inputs = dict(zip(EXPECTED_COMPONENTS, WORK_NAMES, strict=True))
    input_modes: dict[str, str] = {}
    for component, work_name in expected_inputs.items():
        local_input = rf"\input{{tex/works/{work_name}}}"
        shared_input = rf"\input{{../english/tex/works/{work_name}}}"
        local_count = compact[component].count(local_input)
        shared_count = compact[component].count(shared_input)
        if shared_count != 1 or local_count:
            raise RuntimeError(
                f"{component} must input the shared annotated corpus exactly once: {work_name}"
            )
        input_modes[component] = "shared_annotated_corpus"
    required = {
        "W01_witness_note_empty": (
            "W01",
            r"\renewcommand{\GalWitnessNote}[3]{}",
        ),
        "W02_copy_marks_empty": (
            "W02",
            r"\renewcommand{\GalCopySpecificMarks}[4]{}",
        ),
        "W02_copy_image_empty": (
            "W02",
            r"\renewcommand{\GalCopySpecificMarkImage}[4]{}",
        ),
        "W03_copy_image_empty": (
            "W03",
            r"\renewcommand{\GalCopySpecificMarkImage}[4]{}",
        ),
        "W08_variant_first_arg": (
            "W08",
            r"\renewcommand{\GalWitnessVariant}[2]{#1}",
        ),
        "W09_variant_first_arg": (
            "W09",
            r"\renewcommand{\GalWitnessVariant}[2]{#1}",
        ),
        "W10_variant_first_arg": (
            "W10",
            r"\renewcommand{\GalWitnessVariant}[2]{#1}",
        ),
    }
    for label, (component, wanted) in required.items():
        if wanted not in compact[component]:
            raise RuntimeError(f"Direct wrapper projection failed: {label}")
    all_wrappers = "\n".join(texts.values())
    if "\\ddagger" in all_wrappers or "\\dagger" in all_wrappers:
        raise RuntimeError("A direct wrapper hard-codes a modern dagger marker")
    return {
        "wrappers": 11,
        "work_inputs": 11,
        "work_input_modes": input_modes,
        "required_erasure_overrides": len(required),
        "hard_coded_dagger_or_double_dagger": 0,
        "result": "PASS",
    }


def require_annotated_wrapper_policy(annotated: Path) -> dict[str, object]:
    wrappers = annotated / "tex" / "wrappers"
    expected_inputs = dict(zip(EXPECTED_COMPONENTS, WORK_NAMES, strict=True))
    mappings: dict[str, str] = {}
    for component, work_name in expected_inputs.items():
        text = read_utf8(wrappers / f"{component}.tex", annotated)
        compact = re.sub(r"\s+", "", strip_tex_comments(text))
        expected = rf"\input{{tex/works/{work_name}}}"
        work_inputs = re.findall(r"\\input\{(?:\./)?tex/works/([^}]+)\}", compact)
        if compact.count(expected) != 1 or work_inputs != [work_name]:
            raise RuntimeError(
                f"Annotated wrapper {component} must input only its frozen work body: {work_name}"
            )
        mappings[component] = work_name
    return {
        "wrappers": len(mappings),
        "work_inputs": len(mappings),
        "component_to_work": mappings,
        "result": "PASS",
    }


def flatten_outline(items: list[object]) -> list[str]:
    titles: list[str] = []
    for item in items:
        if isinstance(item, list):
            titles.extend(flatten_outline(item))
        else:
            title = getattr(item, "title", None)
            if isinstance(title, str):
                titles.append(title)
    return titles


def scan_rendered_text(text: str, extractor: str) -> dict[str, object]:
    findings = [label for label, pattern in FORBIDDEN_RENDERED_PATTERNS if pattern.search(text)]
    if findings:
        raise RuntimeError(
            f"Modern apparatus rendered under {extractor}: {', '.join(findings)}"
        )
    return {"extractor": extractor, "characters": len(text), "findings": [], "result": "PASS"}


def _resolve_recorder_path(raw: str, source_root: Path) -> Path:
    normalized = raw.replace("\\", "/")
    if re.match(r"(?i)^[A-Z]:/", normalized) or normalized.startswith("/"):
        candidate = Path(normalized)
    else:
        candidate = source_root.joinpath(*PurePosixPath(normalized).parts)
    return candidate.resolve(strict=False)


def inspect_reader_work_input_graph(
    fls: Path,
    source_root: Path,
    authority_root: Path,
    mode: str,
    *,
    pdf: Path | None = None,
) -> dict[str, object]:
    if mode not in {"direct", "annotated"}:
        raise ValueError(f"Unknown reader input-graph mode: {mode}")
    if fls.is_symlink():
        raise ValueError(f"Symlink recorder file is prohibited: {fls}")
    fls = fls.resolve(strict=True)
    source_root = source_root.resolve(strict=True)
    authority_root = authority_root.resolve(strict=True)
    text = fls.read_text(encoding="utf-8", errors="replace")
    input_lines = [line[6:] for line in text.splitlines() if line.startswith("INPUT ")]
    output_lines = [line[7:] for line in text.splitlines() if line.startswith("OUTPUT ")]
    expected_master_name = DIRECT_MASTER if mode == "direct" else ANNOTATED_MASTER
    expected_master = (source_root / expected_master_name).resolve(strict=True)
    master_hits = {
        _resolve_recorder_path(line, source_root)
        for line in input_lines
        if PurePosixPath(line.replace("\\", "/")).name == expected_master_name
    }
    if master_hits != {expected_master}:
        raise RuntimeError(f"{mode} recorder does not bind the exact staged reader master")
    if pdf is not None:
        pdf = pdf.resolve(strict=True)
        if fls.stem != pdf.stem:
            raise RuntimeError(f"{mode} PDF and recorder stems differ")
        pdf_outputs = {
            _resolve_recorder_path(line, source_root)
            for line in output_lines
            if PurePosixPath(line.replace("\\", "/")).suffix.casefold() == ".pdf"
        }
        if pdf not in pdf_outputs:
            raise RuntimeError(f"{mode} recorder does not bind the supplied PDF output")
    records: list[dict[str, object]] = []
    for name in WORK_NAMES:
        expected = (authority_root / "tex" / "works" / name).resolve(strict=True)
        named_hits = [
            line
            for line in input_lines
            if PurePosixPath(line.replace("\\", "/")).name == name
        ]
        resolved_hits = {_resolve_recorder_path(line, source_root) for line in named_hits}
        if not named_hits or resolved_hits != {expected}:
            raise RuntimeError(
                f"{mode} recorder does not prove the exact frozen work input for {name}: "
                f"records={len(named_hits)}, targets={sorted(str(item) for item in resolved_hits)!r}"
            )
        file_record = {"name": name, "bytes": expected.stat().st_size, "sha256": sha256(expected)}
        records.append(
            {
                **file_record,
                "input_records": len(named_hits),
                "resolved_to_frozen_annotated_authority": True,
            }
        )
    return {
        "recorder_name": fls.name,
        "reader_mode": mode,
        "reader_master": expected_master_name,
        "work_files": len(records),
        "authority_work_set_sha256": authority_set_sha256(records),
        "all_work_inputs_resolve_to_frozen_annotated_authority": True,
        "records": records,
        "result": "PASS",
    }


def inspect_direct_pdf(pdf: Path, exact_doi: str | None) -> dict[str, object]:
    if pdf.is_symlink():
        raise ValueError(f"Symlink PDF is prohibited: {pdf}")
    pdf = pdf.resolve(strict=True)
    reader = PdfReader(str(pdf))
    if reader.is_encrypted:
        raise RuntimeError("Direct reader is encrypted")
    if len(reader.pages) != EXPECTED_DIRECT_PAGES:
        raise RuntimeError(
            f"Direct reader page count is {len(reader.pages)}, expected {EXPECTED_DIRECT_PAGES}"
        )
    metadata = reader.metadata or {}
    title = str(metadata.get("/Title", ""))
    if "Source-Faithful English Translation" not in title:
        raise RuntimeError(f"Unexpected direct-reader PDF title: {title!r}")

    destinations = sorted(reader.named_destinations)
    source_destinations = [name for name in destinations if re.fullmatch(r"source-\d{3}", name)]
    critical_destinations = [name for name in destinations if name.startswith("critical-")]
    work_destinations = [name for name in destinations if re.fullmatch(r"work-W\d{2}\.1", name)]
    if len(source_destinations) != EXPECTED_SOURCE_DESTINATIONS:
        raise RuntimeError("Direct reader has the wrong source-destination count")
    source_hash = sha256_lines(source_destinations)
    if source_hash != SOURCE_DESTINATIONS_SHA256:
        raise RuntimeError("Direct reader source-destination universe changed")
    if critical_destinations:
        raise RuntimeError("Direct reader contains critical-note destinations")
    if len(work_destinations) != 11:
        raise RuntimeError("Direct reader does not contain exactly 11 work destinations")

    outline_titles = flatten_outline(reader.outline)
    work_bookmarks = tuple(title for title in outline_titles if title != "Reader contents")
    if work_bookmarks != EXPECTED_WORK_BOOKMARKS:
        raise RuntimeError(f"Direct-reader work bookmarks changed: {work_bookmarks!r}")

    page_texts = [(page.extract_text() or "") for page in reader.pages]
    blank_pages = tuple(index for index, text in enumerate(page_texts, 1) if not text.strip())
    if blank_pages != EXPECTED_DIRECT_BLANK_PAGES:
        raise RuntimeError(
            f"Direct-reader blank topology changed: {blank_pages!r}"
        )
    pypdf_text = "\n".join(page_texts)
    scans = [scan_rendered_text(pypdf_text, "pypdf")]
    extracted = subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if extracted.returncode:
        raise RuntimeError(
            "pdftotext failed: "
            + extracted.stderr.decode("utf-8", errors="replace")[-1000:]
        )
    poppler_text = extracted.stdout.decode("utf-8", errors="replace")
    scans.append(scan_rendered_text(poppler_text, "pdftotext-layout"))
    doi_universes: dict[str, list[str]] = {}
    if exact_doi:
        for label, text in (("pypdf", pypdf_text), ("pdftotext", poppler_text)):
            doi_universes[label] = require_exact_doi_universe(
                text, exact_doi, "direct reader", label
            )

    media_boxes = []
    for page in reader.pages:
        width = round(float(page.mediabox.width), 3)
        height = round(float(page.mediabox.height), 3)
        media_boxes.append((width, height))
    if len(set(media_boxes)) != 1:
        raise RuntimeError("Direct-reader page boxes are not uniform")

    return {
        "name": pdf.name,
        "bytes": pdf.stat().st_size,
        "sha256": sha256(pdf),
        "pages": len(reader.pages),
        "encrypted": False,
        "pdf_title": title,
        "source_destinations": len(source_destinations),
        "source_destination_list_sha256": source_hash,
        "critical_destinations": 0,
        "work_destinations": len(work_destinations),
        "work_bookmarks": list(work_bookmarks),
        "blank_pages": list(blank_pages),
        "uniform_media_box_points": list(media_boxes[0]),
        "rendered_modern_apparatus_scans": scans,
        "exact_doi_checked": exact_doi,
        "doi_universes": doi_universes,
        "result": "PASS",
    }


def validate_projection(
    publication_root: Path,
    *,
    pdf: Path | None = None,
    fls: Path | None = None,
    exact_doi: str | None = None,
) -> dict[str, object]:
    root = publication_root.resolve(strict=True)
    annotated = (root / "source" / "english").resolve(strict=True)
    direct = (root / "source" / "english_direct").resolve(strict=True)
    if not annotated.is_dir() or not direct.is_dir():
        raise NotADirectoryError("Both annotated and direct source roots are required")

    authority = load_frozen_authority()
    english_authority = authority["english_annotated_predecessor"]
    assert isinstance(english_authority, dict)
    frozen_work_records = {
        str(item["name"]): item for item in english_authority["work_files"]
    }
    frozen_figure_records = {
        str(item["name"]): item for item in english_authority["figure_files"]
    }
    annotated_master = read_utf8(annotated / ANNOTATED_MASTER, annotated)
    direct_master = read_utf8(direct / DIRECT_MASTER, direct)
    annotated_master_pin = validate_annotated_master_against_predecessor(
        annotated_master, english_authority["annotated_master"]
    )
    master_policy = require_master_policy(direct_master)
    wrapper_policy = require_wrapper_policy(direct)
    annotated_wrapper_policy = require_annotated_wrapper_policy(annotated)
    if exact_doi is not None:
        require_exact_doi_universe(annotated_master, exact_doi, "annotated source", "TeX")
        require_exact_doi_universe(direct_master, exact_doi, "direct source", "TeX")

    annotated_inputs = re.findall(r"\\input\{tex/wrappers/(W\d{2})\.tex\}", annotated_master)
    direct_inputs = re.findall(r"\\input\{tex/wrappers/(W\d{2})\.tex\}", direct_master)
    if tuple(annotated_inputs) != EXPECTED_COMPONENTS or tuple(direct_inputs) != EXPECTED_COMPONENTS:
        raise RuntimeError("A reader master changed the ordered eleven-component universe")

    work_records: list[dict[str, object]] = []
    annotated_texts: list[str] = []
    inactive_snapshot_records: list[dict[str, object]] = []
    for component, name in zip(EXPECTED_COMPONENTS, WORK_NAMES, strict=True):
        annotated_path = require_file(annotated / "tex" / "works" / name, annotated)
        frozen_record = frozen_file_record(
            annotated_path, frozen_work_records[name], annotated
        )
        annotated_hash = str(frozen_record["sha256"])
        annotated_texts.append(annotated_path.read_text(encoding="utf-8"))
        direct_path = direct / "tex" / "works" / name
        inactive_copy_match: bool | None = None
        if direct_path.exists():
            direct_resolved = require_file(direct_path, direct)
            direct_hash = sha256(direct_resolved)
            inactive_copy_match = (annotated_path.stat().st_size, annotated_hash) == (
                direct_resolved.stat().st_size,
                direct_hash,
            )
            if not inactive_copy_match:
                raise RuntimeError(
                    f"Inactive direct-tree work snapshot diverged from authority: {component}"
                )
            inactive_snapshot_records.append(
                {
                    "component": component,
                    "name": name,
                    "bytes": direct_resolved.stat().st_size,
                    "sha256": direct_hash,
                    "excluded_from_active_projection": True,
                }
            )
        work_records.append(
            {
                "component": component,
                "name": name,
                "bytes": frozen_record["bytes"],
                "sha256": annotated_hash,
                "active_direct_input": "shared annotated corpus",
                "inactive_snapshot_present_and_identical": inactive_copy_match,
            }
        )

    figure_records: list[dict[str, object]] = []
    for name in FIGURE_NAMES:
        annotated_path = require_file(annotated / "figures" / name, annotated)
        direct_path = require_file(direct / "figures" / name, direct)
        frozen_record = frozen_file_record(
            annotated_path, frozen_figure_records[name], annotated
        )
        digest = str(frozen_record["sha256"])
        if (annotated_path.stat().st_size, digest) != (
            direct_path.stat().st_size,
            sha256(direct_path),
        ):
            raise RuntimeError(f"Source-era figure diverged in direct projection: {name}")
        figure_records.append(
            frozen_record
        )

    annotated_work_text = "\n".join(annotated_texts)
    direct_work_text = annotated_work_text
    annotated_segments = [":".join(match) for match in SEGMENT_RE.findall(annotated_work_text)]
    direct_segments = [":".join(match) for match in SEGMENT_RE.findall(direct_work_text)]
    if len(annotated_segments) != EXPECTED_SEGMENTS or len(set(annotated_segments)) != EXPECTED_SEGMENTS:
        raise RuntimeError("Annotated corpus does not have exactly 587 unique ENSEG anchors")
    if direct_segments != annotated_segments:
        raise RuntimeError("Direct projection changed the ordered ENSEG anchor universe")
    components = tuple(dict.fromkeys(segment.split(":", 1)[0] for segment in annotated_segments))
    if components != EXPECTED_COMPONENTS:
        raise RuntimeError(f"Unexpected component order in ENSEG anchors: {components!r}")

    historical_counts = {
        name: macro_call_count(annotated_work_text, name)
        for name in EXPECTED_HISTORICAL_CALLS
    }
    if historical_counts != EXPECTED_HISTORICAL_CALLS:
        raise RuntimeError(f"Historical apparatus count changed: {historical_counts!r}")
    direct_historical_counts = {
        name: macro_call_count(direct_work_text, name)
        for name in EXPECTED_HISTORICAL_CALLS
    }
    if direct_historical_counts != EXPECTED_HISTORICAL_CALLS:
        raise RuntimeError("Direct projection lost source-integral historical apparatus")

    modern_counts = {
        name: macro_call_count(annotated_work_text, name)
        for name in EXPECTED_MODERN_CALLS
    }
    if modern_counts != EXPECTED_MODERN_CALLS:
        raise RuntimeError(f"Modern apparatus source count changed: {modern_counts!r}")
    if {
        name: macro_call_count(direct_work_text, name) for name in EXPECTED_MODERN_CALLS
    } != EXPECTED_MODERN_CALLS:
        raise RuntimeError("Direct source is no longer an exact apparatus-erasing projection")

    if (pdf is None) != (fls is None):
        raise ValueError("PDF validation requires both the PDF and its matching .fls recorder")
    input_graph = (
        inspect_reader_work_input_graph(
            fls, direct, annotated, "direct", pdf=pdf
        )
        if fls is not None
        else None
    )
    pdf_result = inspect_direct_pdf(pdf, exact_doi) if pdf is not None else None
    receipt = {
        "schema_version": 1,
        "receipt_role": "Galois English source-faithful projection validation",
        "result": "PASS",
        "components": len(work_records),
        "component_order": list(EXPECTED_COMPONENTS),
        "aligned_segments": len(annotated_segments),
        "segment_list_sha256": sha256_lines(annotated_segments),
        "work_body_hash_equality": work_records,
        "inactive_direct_work_snapshots": inactive_snapshot_records,
        "source_era_figure_hash_equality": figure_records,
        "historical_apparatus_preserved": historical_counts,
        "modern_apparatus_calls_retained_in_shared_source_but_rendered_empty": modern_counts,
        "frozen_authority": {
            "name": FROZEN_AUTHORITY_PATH.name,
            "bytes": FROZEN_AUTHORITY_PATH.stat().st_size,
            "sha256": sha256(FROZEN_AUTHORITY_PATH),
            "work_set_sha256": authority_set_sha256(work_records),
            "figure_set_sha256": authority_set_sha256(figure_records),
            "annotated_master_pin": annotated_master_pin,
            "result": "PASS",
        },
        "direct_master_erasure_policy": master_policy,
        "direct_wrapper_erasure_policy": wrapper_policy,
        "annotated_wrapper_input_policy": annotated_wrapper_policy,
        "annotated_master_sha256": sha256(annotated / ANNOTATED_MASTER),
        "direct_master_sha256": sha256(direct / DIRECT_MASTER),
        "pdf": pdf_result,
        "compiled_input_graph": input_graph,
    }
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Galois English publication root")
    parser.add_argument("--pdf", type=Path, help="Compiled direct-reader PDF")
    parser.add_argument("--fls", type=Path, help="Matching latex recorder (.fls)")
    parser.add_argument("--exact-doi", help="Require this exact DOI in the PDF")
    parser.add_argument("--receipt", type=Path, help="Write a new JSON receipt")
    args = parser.parse_args()
    if args.exact_doi and args.pdf is None:
        parser.error("--exact-doi requires --pdf")
    if (args.pdf is None) != (args.fls is None):
        parser.error("--pdf and --fls must be supplied together")
    receipt = validate_projection(
        args.root, pdf=args.pdf, fls=args.fls, exact_doi=args.exact_doi
    )
    payload = (json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    if args.receipt:
        target = args.receipt.resolve(strict=False)
        if not target.parent.is_dir():
            raise FileNotFoundError(f"Receipt parent does not exist: {target.parent}")
        with target.open("xb") as stream:
            stream.write(payload)
    print(payload.decode("utf-8"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
