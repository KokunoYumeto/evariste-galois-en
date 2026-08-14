#!/usr/bin/env python3
"""Build the six-file Galois English R3 two-reader release deterministically.

The script never deletes, cleans, reuses, publishes, invokes Git, or reads a
credential.  It first supports a reader-only build for final visual QA, then two
fresh full builds whose six public files must compare byte-for-byte.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import unicodedata
import zipfile
from dataclasses import dataclass
from datetime import date as calendar_date
from pathlib import Path, PurePosixPath
from typing import BinaryIO, Iterable

from pypdf import PdfReader

from validate_galois_english_direct_projection import (
    EXPECTED_WORK_BOOKMARKS,
    FROZEN_AUTHORITY_PATH,
    SOURCE_DESTINATIONS_SHA256,
    inspect_reader_work_input_graph,
    load_frozen_authority,
    require_exact_doi_universe,
    sha256_lines,
    validate_projection,
)


SCRIPT_ROOT = Path(__file__).resolve().parent
DEFAULT_PUBLICATION_ROOT = SCRIPT_ROOT.parent / "galois-en-publication"
DEFAULT_SIBLING_RELEASE = (
    SCRIPT_ROOT.parent
    / "french-r2-reciprocal-builder"
    / "outputs"
    / "fr-r2-humanmeta-verified-20260814T032200000"
)
DEFAULT_PREDECESSOR_EVIDENCE = (
    DEFAULT_PUBLICATION_ROOT
    / "reader-r2-final-verified-20260814T024700000"
    / "02_GALOIS_1897_EN_EVIDENCE_AND_PROVENANCE.zip"
)

CONCEPT_DOI = "10.5281/zenodo.21924301"
FRENCH_CONCEPT_DOI = "10.5281/zenodo.21923856"
FRENCH_EXACT_DOI = "10.5281/zenodo.21925876"
ANNOTATED_PREDECESSOR_DOI = "10.5281/zenodo.21926209"
ANNOTATED_PREDECESSOR_READER_SHA256 = (
    "2AF04298A1184307C2F94B82FAE55E6AA0BDA4560C2E95461537924AB814E6D5"
)
PREDECESSOR_EVIDENCE_SHA256 = (
    "A16FA574C3F713894A1E53EE77C79A3BE662DB569CF572A748379FC05AA0F031"
)

DIRECT_READER_NAME = "00_GALOIS_1897_EN_SOURCE_FAITHFUL_READER.pdf"
ANNOTATED_READER_NAME = "01_GALOIS_1897_EN_GPT_ANNOTATED_READER.pdf"
SOURCE_ZIP_NAME = "02_GALOIS_1897_EN_EDITABLE_SOURCES.zip"
EVIDENCE_ZIP_NAME = "03_GALOIS_1897_EN_EVIDENCE_AND_PROVENANCE.zip"
MANIFEST_NAME = "04_GALOIS_1897_EN_SHA256_MANIFEST.txt"
OTHER_TRANSLATIONS_NAME = "OTHER_TRANSLATIONS.zip"
PUBLIC_NAMES = (
    DIRECT_READER_NAME,
    ANNOTATED_READER_NAME,
    SOURCE_ZIP_NAME,
    EVIDENCE_ZIP_NAME,
    MANIFEST_NAME,
    OTHER_TRANSLATIONS_NAME,
)
MANIFEST_PAYLOAD_NAMES = (
    DIRECT_READER_NAME,
    ANNOTATED_READER_NAME,
    SOURCE_ZIP_NAME,
    EVIDENCE_ZIP_NAME,
    OTHER_TRANSLATIONS_NAME,
)
SIBLING_PUBLIC_NAMES = (
    "00_GALOIS_1897_FR_CURRENT_LINKED_READER.pdf",
    "01_GALOIS_1897_FR_EDITABLE_SOURCES.zip",
    "02_GALOIS_1897_FR_EVIDENCE_AND_PROVENANCE.zip",
    "03_GALOIS_1897_FR_SHA256_MANIFEST.txt",
    "OTHER_TRANSLATIONS.zip",
)

ANNOTATED_MASTER = "GAL1897_EN_MODERN_READER.tex"
DIRECT_MASTER = "GAL1897_EN_SOURCE_FAITHFUL_READER.tex"
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
ANNOTATED_SOURCE_FILES = (
    ANNOTATED_MASTER,
    "STYLE_GUIDE.md",
    *(f"figures/{name}" for name in FIGURE_NAMES),
    *(f"tex/works/{name}" for name in WORK_NAMES),
    *(f"tex/wrappers/W{number:02d}.tex" for number in range(1, 12)),
)
# The direct reader must use ../english/tex/works.  Inactive copied work files and
# the literal historical "$build" accident are intentionally not staged/packageable.
DIRECT_SOURCE_FILES = (
    DIRECT_MASTER,
    "STYLE_GUIDE.md",
    *(f"figures/{name}" for name in FIGURE_NAMES),
    *(f"tex/wrappers/W{number:02d}.tex" for number in range(1, 12)),
)

FIXED_ZIP_TIME = (2026, 8, 14, 0, 0, 0)
ZIP_LEVEL = 9
BLOCK_SIZE = 1024 * 1024
SCAN_OVERLAP = 4096
SAFE_LEAF = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
DOS_RESERVED = re.compile(r"(?i)(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?\Z")
EXACT_DOI_RE = re.compile(r"10\.5281/zenodo\.(\d+)\Z")
VERSION_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9 ._+-]{0,127}\Z")
TAG_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]{0,127}\Z")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")
METADATA_FILE_NAMES = (
    ".zenodo.json",
    "CITATION.cff",
    "DATACITE_RELATIONS.json",
    "PUBLICATION_IDENTITY.json",
    "README.md",
    "RELEASE_SURFACE.md",
    "RIGHTS_AND_LICENSING.md",
    "METADATA_RENDER_RECEIPT.json",
)
METADATA_RENDERED_NAMES = METADATA_FILE_NAMES[:-1]
PUBLIC_TITLE = (
    "Évariste Galois — Mathematical Works (1897): "
    "Source-Faithful English Translation and GPT-Annotated Edition"
)
VISUAL_QA_SCHEMA_PATH = SCRIPT_ROOT / "GALOIS_R3_VISUAL_QA_RECEIPT_SCHEMA.json"

ABSOLUTE_PATH_PATTERNS = (
    ("windows_absolute_path", re.compile(rb"(?i)(?<![A-Za-z0-9+.-])[A-Z]:[\\/]")),
    ("windows_unc_path", re.compile(rb"(?<![\\])\\\\[A-Za-z0-9._$-]+[\\/][A-Za-z0-9._$-]+")),
    ("unix_private_absolute_path", re.compile(rb"(?i)(?<![A-Za-z0-9])/(?:home|Users|tmp|var/tmp)/")),
    ("local_file_uri", re.compile(rb"(?i)file:" + rb"///")),
)
PDF_ABSOLUTE_PATH_PATTERNS = (
    (
        "personal_windows_absolute_path",
        re.compile(
            rb"(?i)(?<![A-Za-z0-9+.-])[A-Z]:[\\/]"
            rb"(?:Users|Documents|Temp|tmp|home)[\\/]"
        ),
    ),
    (
        "printable_windows_absolute_path",
        re.compile(
            rb"(?i)(?<![A-Za-z0-9+.-])[A-Z]:[\\/]"
            rb"[A-Za-z0-9_. -]{1,64}[\\/][A-Za-z0-9_. -]{1,64}"
        ),
    ),
    ABSOLUTE_PATH_PATTERNS[1],
    ABSOLUTE_PATH_PATTERNS[2],
    ABSOLUTE_PATH_PATTERNS[3],
)
SECRET_PATTERNS = (
    ("github_fine_grained_token", re.compile(rb"github" + rb"_pat_[A-Za-z0-9_]{20,}")),
    ("github_classic_token", re.compile(rb"gh" + rb"[pousr]_[A-Za-z0-9]{20,}")),
    ("bearer_token", re.compile(rb"(?i)Authorization\s*:\s*Bearer\s+[A-Za-z0-9._~+/=-]{20,}")),
    ("assigned_secret", re.compile(rb"(?i)\b(?:access[_-]?token|api[_-]?key|client[_-]?secret|password|passwd)[\"']?\s*[=:]\s*[\"']?[A-Za-z0-9._~+/=-]{12,}")),
    ("private_key_material", re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
)
OPAQUE_SUFFIXES = {".zip"}
STRONG_BINARY_SUFFIXES = {".pdf", ".png", ".jpg", ".jpeg", ".jp2", ".tif", ".tiff"}

ANNOTATED_EXPECTED_PAGES = 84
ANNOTATED_EXPECTED_BLANKS = (41, 79, 82, 83, 84)
ANNOTATED_CRITICAL_DESTINATIONS = 65
ANNOTATED_CRITICAL_DESTINATIONS_SHA256 = (
    "8BE333B27443E8CD834DA99E3D5638FA5276B784E1C28C0EEF086C5FE310F7DB"
)


@dataclass(frozen=True)
class Entry:
    name: str
    size: int
    digest: str
    source: Path | None = None
    data: bytes | None = None

    def record(self) -> dict[str, object]:
        return {"name": self.name, "bytes": self.size, "sha256": self.digest}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(BLOCK_SIZE), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def validate_leaf(value: str, option: str) -> str:
    if not SAFE_LEAF.fullmatch(value) or DOS_RESERVED.fullmatch(value):
        raise ValueError(f"{option} must be one safe relative directory name")
    return value


def validate_identity(exact_doi: str, version: str, tag: str, publication_date: str) -> None:
    match = EXACT_DOI_RE.fullmatch(exact_doi)
    if not match or exact_doi in {CONCEPT_DOI, ANNOTATED_PREDECESSOR_DOI}:
        raise ValueError("--exact-doi must be a new Zenodo version DOI in the English lineage")
    if not VERSION_RE.fullmatch(version):
        raise ValueError("--version is not a safe release label")
    if not TAG_RE.fullmatch(tag):
        raise ValueError("--tag is not a safe Git tag label")
    if not DATE_RE.fullmatch(publication_date):
        raise ValueError("--publication-date must be YYYY-MM-DD")
    try:
        calendar_date.fromisoformat(publication_date)
    except ValueError as error:
        raise ValueError("--publication-date is not a real calendar date") from error


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root.resolve(strict=True))
        return True
    except ValueError:
        return False


def ensure_within(path: Path, root: Path) -> None:
    if not is_within(path.resolve(strict=False), root):
        raise ValueError(f"Path escapes declared root: {path}")


def require_file(path: Path, roots: Iterable[Path]) -> Path:
    if path.is_symlink():
        raise ValueError(f"Symlink input is prohibited: {path}")
    resolved = path.resolve(strict=True)
    if not resolved.is_file() or not any(is_within(resolved, root) for root in roots):
        raise FileNotFoundError(f"Required regular input is unavailable: {path}")
    return resolved


def claim_directory(path: Path, root: Path) -> None:
    ensure_within(path, root)
    if path.exists():
        raise FileExistsError(f"Refusing to reuse any directory: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.mkdir()


def write_new(path: Path, data: bytes, root: Path) -> None:
    ensure_within(path, root)
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(data)


def copy_new(source: Path, target: Path, root: Path) -> None:
    ensure_within(target, root)
    if target.exists():
        raise FileExistsError(f"Refusing to overwrite: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    with source.open("rb") as incoming, target.open("xb") as outgoing:
        shutil.copyfileobj(incoming, outgoing, length=BLOCK_SIZE)


def validate_member_name(name: str) -> None:
    if not name or "\x00" in name or "\\" in name or name.startswith("/"):
        raise ValueError(f"Unsafe ZIP member name: {name!r}")
    if re.match(r"(?i)^[A-Z]:", name):
        raise ValueError(f"Absolute ZIP member name: {name!r}")
    if unicodedata.normalize("NFC", name) != name:
        raise ValueError(f"Non-NFC ZIP member name: {name!r}")
    parts = name.split("/")
    if any(part in {"", ".", ".."} or part.endswith((" ", ".")) for part in parts):
        raise ValueError(f"Non-canonical ZIP member name: {name!r}")
    if any(DOS_RESERVED.fullmatch(part) for part in parts):
        raise ValueError(f"Platform-reserved ZIP member name: {name!r}")
    if PurePosixPath(name).as_posix() != name:
        raise ValueError(f"Non-POSIX ZIP member name: {name!r}")


def validate_member_set(names: list[str], ordered: bool) -> None:
    for name in names:
        validate_member_name(name)
    if len(names) != len(set(names)):
        raise ValueError("Duplicate ZIP member names")
    normalized: dict[str, str] = {}
    for name in names:
        key = unicodedata.normalize("NFC", name).casefold()
        if key in normalized:
            raise ValueError(f"Case/Unicode ZIP collision: {normalized[key]!r}, {name!r}")
        normalized[key] = name
    if ordered and names != sorted(names):
        raise ValueError("ZIP member order is not canonical")


def entry_from_file(path: Path, name: str, roots: Iterable[Path]) -> Entry:
    validate_member_name(name)
    source = require_file(path, roots)
    return Entry(name, source.stat().st_size, sha256(source), source=source)


def entry_from_data(data: bytes, name: str) -> Entry:
    validate_member_name(name)
    return Entry(name, len(data), sha256_bytes(data), data=data)


def assert_entries_unchanged(entries: Iterable[Entry]) -> None:
    for entry in entries:
        if entry.source is not None and (entry.source.stat().st_size, sha256(entry.source)) != (
            entry.size,
            entry.digest,
        ):
            raise RuntimeError(f"Input changed during build: {entry.name}")


def scan_chunks(chunks: Iterable[bytes], include_absolute_paths: bool) -> tuple[str, ...]:
    patterns = SECRET_PATTERNS + (ABSOLUTE_PATH_PATTERNS if include_absolute_paths else ())
    hits: set[str] = set()
    carry = b""
    for chunk in chunks:
        block = carry + chunk
        for label, pattern in patterns:
            if pattern.search(block):
                hits.add(label)
        carry = block[-SCAN_OVERLAP:]
    return tuple(sorted(hits))


def scan_patterns_for_name(name: str, include_absolute_paths: bool) -> tuple[tuple[str, re.Pattern[bytes]], ...]:
    suffix = PurePosixPath(name).suffix.casefold()
    absolute = PDF_ABSOLUTE_PATH_PATTERNS if suffix in STRONG_BINARY_SUFFIXES else ABSOLUTE_PATH_PATTERNS
    return SECRET_PATTERNS + (absolute if include_absolute_paths else ())


def scan_entry(entry: Entry, include_absolute_paths: bool = True) -> tuple[str, ...]:
    if PurePosixPath(entry.name).suffix.casefold() in OPAQUE_SUFFIXES:
        return ()
    patterns = scan_patterns_for_name(entry.name, include_absolute_paths)
    def scan(chunks: Iterable[bytes]) -> tuple[str, ...]:
        hits: set[str] = set()
        carry = b""
        for chunk in chunks:
            block = carry + chunk
            for label, pattern in patterns:
                if pattern.search(block):
                    hits.add(label)
            carry = block[-SCAN_OVERLAP:]
        return tuple(sorted(hits))
    if entry.data is not None:
        return scan((entry.data,))
    assert entry.source is not None
    with entry.source.open("rb") as stream:
        return scan(iter(lambda: stream.read(BLOCK_SIZE), b""))


def assert_entries_safe(entries: Iterable[Entry], context: str, include_absolute_paths: bool = True) -> None:
    for entry in entries:
        hits = scan_entry(entry, include_absolute_paths)
        if hits:
            raise RuntimeError(f"Public-safety scan failed in {context}/{entry.name}: {', '.join(hits)}")


def write_zip(path: Path, root: Path, entries: list[Entry]) -> None:
    ensure_within(path, root)
    if path.exists():
        raise FileExistsError(path)
    ordered = sorted(entries, key=lambda item: item.name)
    validate_member_set([entry.name for entry in ordered], ordered=True)
    assert_entries_unchanged(ordered)
    with zipfile.ZipFile(
        path,
        "x",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=ZIP_LEVEL,
        allowZip64=True,
        strict_timestamps=True,
    ) as archive:
        archive.comment = b""
        for entry in ordered:
            info = zipfile.ZipInfo(entry.name, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_STORED if entry.name.endswith(".zip") else zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.internal_attr = 0
            info.extra = b""
            info.comment = b""
            info.file_size = entry.size
            info._compresslevel = ZIP_LEVEL
            with archive.open(info, "w", force_zip64=True) as member:
                if entry.data is not None:
                    member.write(entry.data)
                else:
                    assert entry.source is not None
                    with entry.source.open("rb") as source:
                        shutil.copyfileobj(source, member, length=BLOCK_SIZE)


def inspect_zip(
    path: Path,
    expected: dict[str, tuple[int, str]] | None,
    *,
    scan_content: bool,
    scan_absolute_paths: bool,
    require_fixed_time: bool,
    require_order: bool,
) -> dict[str, object]:
    records: list[tuple[str, int, str]] = []
    with zipfile.ZipFile(path) as archive:
        if archive.comment:
            raise RuntimeError(f"ZIP comments are prohibited: {path.name}")
        names = archive.namelist()
        validate_member_set(names, ordered=require_order)
        if expected is not None and set(names) != set(expected):
            raise RuntimeError(f"ZIP member-set mismatch: {path.name}")
        failure = archive.testzip()
        if failure:
            raise RuntimeError(f"ZIP CRC failure: {failure}")
        for info in archive.infolist():
            mode = info.external_attr >> 16
            if info.is_dir() or info.flag_bits & 1 or (mode and not stat.S_ISREG(mode)):
                raise RuntimeError(f"Unsafe ZIP member metadata: {info.filename}")
            if require_fixed_time and info.date_time != FIXED_ZIP_TIME:
                raise RuntimeError(f"Non-deterministic ZIP timestamp: {info.filename}")
            digest = hashlib.sha256()
            size = 0
            labels: set[str] = set()
            carry = b""
            with archive.open(info) as member:
                for block in iter(lambda: member.read(BLOCK_SIZE), b""):
                    digest.update(block)
                    size += len(block)
                    if scan_content and PurePosixPath(info.filename).suffix.casefold() not in OPAQUE_SUFFIXES:
                        combined = carry + block
                        for label, pattern in scan_patterns_for_name(
                            info.filename, scan_absolute_paths
                        ):
                            if pattern.search(combined):
                                labels.add(label)
                        carry = combined[-SCAN_OVERLAP:]
            actual = digest.hexdigest().upper()
            if labels:
                raise RuntimeError(f"Unsafe content inside {path.name}/{info.filename}: {sorted(labels)}")
            if expected is not None and expected[info.filename] != (size, actual):
                raise RuntimeError(f"ZIP member hash mismatch: {info.filename}")
            records.append((info.filename, size, actual))
    return {
        "entries": len(records),
        "payload_bytes": sum(size for _, size, _ in records),
        "member_list_sha256": sha256_lines(
            f"{name}\t{size}\t{digest}" for name, size, digest in sorted(records)
        ),
        "crc": "PASS",
        "duplicates": 0,
        "casefold_collisions": 0,
        "symlinks": 0,
        "encrypted_members": 0,
        "unsafe_paths": 0,
        "secret_findings": 0,
        "absolute_path_findings": 0 if scan_absolute_paths else "NOT_CLAIMED_FOR_FROZEN_NESTED_PAYLOAD",
        "result": "PASS",
    }


def inject_exact_doi(text: str, exact_doi: str, role: str) -> str:
    line = (
        r"{\small Exact release DOI: \href{https://doi.org/"
        + exact_doi
        + "}{"
        + exact_doi
        + r"}\par}"
    )
    pattern = re.compile(
        r"(?m)^(?P<indent>[ \t]*)\{\\small Exact release DOI:.*?\\par\}(?P<trailing>[ \t]*)$"
    )
    if pattern.search(text):
        text, count = pattern.subn(
            lambda match: match.group("indent") + line + match.group("trailing"),
            text,
            count=1,
        )
        if count != 1:
            raise RuntimeError(f"Could not replace {role} exact DOI line")
    elif role == "direct":
        concept_pattern = re.compile(
            r"(?m)^(\s*\{\\small English concept DOI:.*?\\par\}\s*)$"
        )
        text, count = concept_pattern.subn(
            lambda match: match.group(1) + "\n" + line,
            text,
            count=1,
        )
        if count != 1:
            raise RuntimeError("Could not insert direct-reader exact DOI line")
    else:
        raise RuntimeError("Annotated source has no replaceable exact DOI line")
    if text.count(exact_doi) != 2:
        raise RuntimeError(f"{role} source must contain the exact DOI exactly twice")
    require_exact_doi_universe(text, exact_doi, f"{role} source", "TeX")
    if ANNOTATED_PREDECESSOR_DOI in text:
        raise RuntimeError(f"{role} staged source retained the predecessor exact DOI")
    return text


def stage_sources(root: Path, build: Path, exact_doi: str) -> tuple[Path, list[Entry]]:
    staged_root = build / "staged-publication"
    source_root = staged_root / "source"
    source_root.mkdir(parents=True)
    original_entries: list[Entry] = []
    for role, directory, names, master in (
        ("annotated", "english", ANNOTATED_SOURCE_FILES, ANNOTATED_MASTER),
        ("direct", "english_direct", DIRECT_SOURCE_FILES, DIRECT_MASTER),
    ):
        original = root / "source" / directory
        staged = source_root / directory
        staged.mkdir()
        for relative in names:
            source = require_file(original / relative, (original,))
            original_entries.append(entry_from_file(source, f"{directory}/{relative}", (original,)))
            target = staged / relative
            if relative == master:
                rendered = inject_exact_doi(source.read_text(encoding="utf-8"), exact_doi, role)
                write_new(target, rendered.encode("utf-8"), staged_root)
            else:
                copy_new(source, target, staged_root)
    assert_entries_unchanged(original_entries)
    return staged_root, original_entries


def run_latex(source: Path, master: str, build: Path) -> tuple[Path, Path, dict[str, object]]:
    build.mkdir(parents=True)
    console = build / "latexmk-console.txt"
    environment = os.environ.copy()
    environment["SOURCE_DATE_EPOCH"] = "1786665600"
    environment["TZ"] = "UTC"
    command = [
        "latexmk",
        "-pdf",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        f"-outdir={build}",
        master,
    ]
    result = subprocess.run(
        command,
        cwd=source,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    write_new(console, result.stdout, build)
    if result.returncode:
        raise RuntimeError(
            f"LaTeX failed for {master}: "
            + result.stdout.decode("utf-8", errors="replace")[-3000:]
        )
    stem = Path(master).stem
    pdf = require_file(build / f"{stem}.pdf", (build,))
    fls = require_file(build / f"{stem}.fls", (build,))
    log = require_file(build / f"{stem}.log", (build,))
    log_text = log.read_text(encoding="utf-8", errors="replace")
    warning_patterns = (
        r"LaTeX Warning:",
        r"Package \S+ Warning:",
        r"Overfull \\hbox",
        r"Underfull \\hbox",
        r"destination with the same identifier",
        r"undefined references?",
    )
    warnings = [pattern for pattern in warning_patterns if re.search(pattern, log_text, re.I)]
    if warnings:
        raise RuntimeError(f"Final LaTeX log contains warnings for {master}: {warnings}")
    return pdf, fls, {
        "master": master,
        "pdf": {"bytes": pdf.stat().st_size, "sha256": sha256(pdf)},
        "fls_sha256": sha256(fls),
        "log_sha256": sha256(log),
        "console_sha256": sha256(console),
        "warnings": 0,
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


def inspect_annotated_pdf(pdf: Path, exact_doi: str) -> dict[str, object]:
    reader = PdfReader(str(pdf))
    if reader.is_encrypted or len(reader.pages) != ANNOTATED_EXPECTED_PAGES:
        raise RuntimeError("Annotated reader encryption/page-count gate failed")
    title = str((reader.metadata or {}).get("/Title", ""))
    if "Modern English Reader with Editorial Notes" not in title:
        raise RuntimeError(f"Unexpected annotated-reader title: {title!r}")
    names = sorted(reader.named_destinations)
    sources = [name for name in names if re.fullmatch(r"source-\d{3}", name)]
    critical = [name for name in names if name.startswith("critical-")]
    works = [name for name in names if re.fullmatch(r"work-W\d{2}\.1", name)]
    if len(sources) != 73 or sha256_lines(sources) != SOURCE_DESTINATIONS_SHA256:
        raise RuntimeError("Annotated source-destination universe changed")
    if (
        len(critical) != ANNOTATED_CRITICAL_DESTINATIONS
        or sha256_lines(critical) != ANNOTATED_CRITICAL_DESTINATIONS_SHA256
    ):
        raise RuntimeError("Annotated critical-destination universe changed")
    if len(works) != 11:
        raise RuntimeError("Annotated work-destination count changed")
    outline = flatten_outline(reader.outline)
    if tuple(title for title in outline if title != "Reader contents") != EXPECTED_WORK_BOOKMARKS:
        raise RuntimeError("Annotated work bookmarks changed")
    page_text = [(page.extract_text() or "") for page in reader.pages]
    blanks = tuple(index for index, text in enumerate(page_text, 1) if not text.strip())
    if blanks != ANNOTATED_EXPECTED_BLANKS:
        raise RuntimeError(f"Annotated blank topology changed: {blanks!r}")
    pypdf_text = "\n".join(page_text)
    extracted = subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if extracted.returncode:
        raise RuntimeError("pdftotext failed on annotated reader")
    poppler_text = extracted.stdout.decode("utf-8", errors="replace")
    doi_universes: dict[str, list[str]] = {}
    for label, text in (("pypdf", pypdf_text), ("pdftotext", poppler_text)):
        doi_universes[label] = require_exact_doi_universe(
            text, exact_doi, "annotated reader", label
        )
    boxes = {
        (round(float(page.mediabox.width), 3), round(float(page.mediabox.height), 3))
        for page in reader.pages
    }
    if len(boxes) != 1:
        raise RuntimeError("Annotated page boxes are not uniform")
    return {
        "name": pdf.name,
        "bytes": pdf.stat().st_size,
        "sha256": sha256(pdf),
        "pages": len(reader.pages),
        "encrypted": False,
        "pdf_title": title,
        "source_destinations": len(sources),
        "source_destination_list_sha256": sha256_lines(sources),
        "critical_destinations": len(critical),
        "critical_destination_list_sha256": sha256_lines(critical),
        "work_destinations": len(works),
        "work_bookmarks": list(EXPECTED_WORK_BOOKMARKS),
        "blank_pages": list(blanks),
        "uniform_media_box_points": list(next(iter(boxes))),
        "exact_doi": exact_doi,
        "doi_universes": doi_universes,
        "two_text_extractors_confirm_identity": True,
        "result": "PASS",
    }


def walk_json(value: object, path: tuple[str, ...] = ()) -> Iterable[tuple[tuple[str, ...], object]]:
    yield path, value
    if isinstance(value, dict):
        for key, item in value.items():
            yield from walk_json(item, path + (str(key),))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from walk_json(item, path + (str(index),))


def bind_visual_receipt(
    path: Path,
    pdf_record: dict[str, object],
    role: str,
    exact_doi: str,
) -> dict[str, object]:
    source = require_file(path, (path.parent.resolve(strict=True),))
    raw = source.read_bytes()
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"{role} QA receipt must be UTF-8 JSON") from error
    if not isinstance(value, dict):
        raise RuntimeError(f"{role} QA receipt must be a JSON object")
    digest = str(pdf_record["sha256"])
    pages = int(pdf_record["pages"])
    expected_claim = {
        "schema_version": 1,
        "receipt_role": "Galois English R3 all-page visual QA",
        "reader_role": role,
        "exact_doi": exact_doi,
        "concept_doi": CONCEPT_DOI,
        "pdf_sha256": digest,
        "page_count": pages,
        "inspected_pages": list(range(1, pages + 1)),
        "all_pages_visually_inspected": True,
        "visual_result": "PASS",
        "blocking_findings": [],
    }
    failures = [
        key for key, expected in expected_claim.items() if value.get(key) != expected
    ]
    if failures:
        raise RuntimeError(
            f"{role} QA receipt violates the strict exact-artifact schema: {failures}"
        )
    return {
        "schema_version": 1,
        "reader_role": role,
        "source_qa_receipt": {
            "name": source.name,
            "bytes": len(raw),
            "sha256": sha256_bytes(raw),
        },
        "reader": pdf_record,
        "validated_claim": expected_claim,
        "exact_pdf_hash_bound": True,
        "exact_page_count_bound": True,
        "all_pages_visually_inspected": True,
        "result": "PASS",
    }


def read_json_object(path: Path, root: Path, role: str) -> tuple[Path, bytes, dict[str, object]]:
    source = require_file(path, (root,))
    raw = source.read_bytes()
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"{role} must be UTF-8 JSON") from error
    if not isinstance(value, dict):
        raise RuntimeError(f"{role} must be a JSON object")
    return source, raw, value


def validate_reservation_identity(
    path: Path,
    exact_doi: str,
    version: str,
    tag: str,
    publication_date: str,
) -> tuple[dict[str, object], Entry]:
    parent = path.parent.resolve(strict=True)
    source, raw, receipt = read_json_object(path, parent, "reservation identity receipt")
    record_id = int(EXACT_DOI_RE.fullmatch(exact_doi).group(1))  # validated by validate_identity
    expected = {
        "schema_version": 1,
        "receipt_role": "Galois English R3 same-concept Zenodo reservation",
        "predecessor_record_id": int(ANNOTATED_PREDECESSOR_DOI.rsplit(".", 1)[1]),
        "predecessor_exact_doi": ANNOTATED_PREDECESSOR_DOI,
        "predecessor_is_current_concept_version": True,
        "new_version_of_record_id": int(ANNOTATED_PREDECESSOR_DOI.rsplit(".", 1)[1]),
        "trusted_latest_draft_link_verified": True,
        "draft_record_id": record_id,
        "reserved_exact_doi": exact_doi,
        "concept_record_id": CONCEPT_DOI.rsplit(".", 1)[1],
        "concept_doi": CONCEPT_DOI,
        "state": "unsubmitted",
        "submitted": False,
        "planned_version": version,
        "planned_tag": tag,
        "planned_publication_date": publication_date,
        "credential_contents_logged": False,
    }
    failures = [key for key, wanted in expected.items() if receipt.get(key) != wanted]
    if receipt.get("action") not in {
        "new_version_draft_created",
        "existing_new_version_draft_reused",
    }:
        failures.append("action")
    if failures:
        raise RuntimeError(f"Reservation identity receipt mismatch: {sorted(set(failures))}")
    return (
        {
            "name": source.name,
            "bytes": len(raw),
            "sha256": sha256_bytes(raw),
            "record_id": record_id,
            "exact_doi": exact_doi,
            "concept_doi": CONCEPT_DOI,
            "result": "PASS",
        },
        entry_from_file(source, "evidence/r3/ZENODO_RESERVATION_IDENTITY.json", (parent,)),
    )


def validate_rendered_metadata(
    directory: Path,
    exact_doi: str,
    version: str,
    tag: str,
    publication_date: str,
) -> tuple[list[Entry], dict[str, object]]:
    if directory.is_symlink():
        raise ValueError("Rendered metadata directory may not be a symlink")
    root = directory.resolve(strict=True)
    if not root.is_dir():
        raise NotADirectoryError(root)
    children = list(root.iterdir())
    if any(item.is_symlink() or not item.is_file() for item in children):
        raise RuntimeError("Rendered metadata directory must contain regular files only")
    if {item.name for item in children} != set(METADATA_FILE_NAMES):
        raise RuntimeError("Rendered metadata directory is not the exact seven-file render set")
    values: dict[str, dict[str, object]] = {}
    raw_by_name: dict[str, bytes] = {}
    for name in (".zenodo.json", "DATACITE_RELATIONS.json", "PUBLICATION_IDENTITY.json", "METADATA_RENDER_RECEIPT.json"):
        _source, raw, value = read_json_object(root / name, root, f"rendered metadata {name}")
        values[name] = value
        raw_by_name[name] = raw
    record_id = int(EXACT_DOI_RE.fullmatch(exact_doi).group(1))
    identity = values["PUBLICATION_IDENTITY.json"]
    expected_identity = {
        "schema_version": 1,
        "title": PUBLIC_TITLE,
        "record_id": record_id,
        "exact_doi": exact_doi,
        "concept_record_id": int(CONCEPT_DOI.rsplit(".", 1)[1]),
        "concept_doi": CONCEPT_DOI,
        "predecessor_record_id": int(ANNOTATED_PREDECESSOR_DOI.rsplit(".", 1)[1]),
        "predecessor_exact_doi": ANNOTATED_PREDECESSOR_DOI,
        "version": version,
        "tag": tag,
        "publication_date": publication_date,
        "repository": "https://github.com/KokunoYumeto/evariste-galois-en",
        "french_concept_doi": FRENCH_CONCEPT_DOI,
    }
    identity_failures = [
        key for key, wanted in expected_identity.items() if identity.get(key) != wanted
    ]
    if identity.get("public_files") != list(PUBLIC_NAMES):
        identity_failures.append("public_files")
    if identity.get("same_record_reader_files") != [DIRECT_READER_NAME, ANNOTATED_READER_NAME]:
        identity_failures.append("same_record_reader_files")
    if identity_failures:
        raise RuntimeError(f"Rendered publication identity mismatch: {identity_failures}")
    metadata = values[".zenodo.json"]
    if (
        metadata.get("title") != PUBLIC_TITLE
        or metadata.get("version") != version
        or metadata.get("publication_date") != publication_date
        or metadata.get("language") != "eng"
        or metadata.get("upload_type") != "publication"
        or metadata.get("publication_type") != "book"
    ):
        raise RuntimeError("Rendered Zenodo metadata identity/type mismatch")
    description = str(metadata.get("description", ""))
    for required in (exact_doi, tag, DIRECT_READER_NAME, ANNOTATED_READER_NAME):
        if required not in description:
            raise RuntimeError(f"Rendered Zenodo description omits required identity: {required}")
    relations = values["DATACITE_RELATIONS.json"]
    identifiers = relations.get("identifiers")
    same_release = relations.get("same_release_assertion")
    if (
        not isinstance(identifiers, dict)
        or identifiers.get("english_exact_version") != exact_doi
        or identifiers.get("english_record_id") != record_id
        or identifiers.get("english_concept") != CONCEPT_DOI
        or identifiers.get("french_concept") != FRENCH_CONCEPT_DOI
        or not isinstance(same_release, dict)
        or same_release.get("doi") != exact_doi
        or same_release.get("version") != version
        or same_release.get("tag") != tag
        or same_release.get("reader_files") != [DIRECT_READER_NAME, ANNOTATED_READER_NAME]
        or same_release.get("separate_reader_dois") is not False
    ):
        raise RuntimeError("Rendered DataCite relation identity mismatch")
    render_receipt = values["METADATA_RENDER_RECEIPT.json"]
    expected_receipt = {
        "schema_version": 1,
        "result": "PASS",
        "record_id": record_id,
        "exact_doi": exact_doi,
        "concept_doi": CONCEPT_DOI,
        "version": version,
        "tag": tag,
        "publication_date": publication_date,
        "title": PUBLIC_TITLE,
        "public_file_count": len(PUBLIC_NAMES),
        "both_reader_files_share_one_exact_doi": True,
    }
    receipt_failures = [
        key for key, wanted in expected_receipt.items() if render_receipt.get(key) != wanted
    ]
    rendered_rows = render_receipt.get("rendered_files")
    if not isinstance(rendered_rows, list):
        receipt_failures.append("rendered_files")
        rendered_rows = []
    row_map = {
        row.get("name"): row for row in rendered_rows if isinstance(row, dict) and isinstance(row.get("name"), str)
    }
    if set(row_map) != set(METADATA_RENDERED_NAMES) or len(rendered_rows) != len(METADATA_RENDERED_NAMES):
        receipt_failures.append("rendered_files")
    for name in METADATA_RENDERED_NAMES:
        source = require_file(root / name, (root,))
        row = row_map.get(name, {})
        if (row.get("bytes"), row.get("sha256")) != (source.stat().st_size, sha256(source)):
            receipt_failures.append(f"rendered_files:{name}")
    if receipt_failures:
        raise RuntimeError(f"Metadata render receipt mismatch: {sorted(set(receipt_failures))}")
    text_requirements = {
        "CITATION.cff": (exact_doi, version, publication_date),
        "README.md": (exact_doi, version, tag),
        "RELEASE_SURFACE.md": (exact_doi, version, tag),
        "RIGHTS_AND_LICENSING.md": (exact_doi, version, tag),
    }
    for name, requirements in text_requirements.items():
        text = require_file(root / name, (root,)).read_text(encoding="utf-8")
        for required in requirements:
            if required not in text:
                raise RuntimeError(f"Rendered metadata {name} omits {required}")
    entries = [entry_from_file(root / name, name, (root,)) for name in METADATA_RENDERED_NAMES]
    validate_member_set([entry.name for entry in entries], ordered=False)
    return entries, {
        "directory_name": root.name,
        "record_id": record_id,
        "exact_doi": exact_doi,
        "files": [entry.record() for entry in entries],
        "render_receipt_sha256": sha256_bytes(raw_by_name["METADATA_RENDER_RECEIPT.json"]),
        "result": "PASS",
    }


def load_predecessor_evidence(path: Path) -> tuple[list[Entry], dict[str, object]]:
    source = require_file(path, (path.parent.resolve(strict=True),))
    if sha256(source) != PREDECESSOR_EVIDENCE_SHA256:
        raise RuntimeError("Published R2 evidence archive hash does not match frozen authority")
    check = inspect_zip(
        source,
        None,
        scan_content=True,
        scan_absolute_paths=True,
        require_fixed_time=True,
        require_order=True,
    )
    entries: list[Entry] = []
    with zipfile.ZipFile(source) as archive:
        for info in archive.infolist():
            data = archive.read(info)
            entries.append(entry_from_data(data, info.filename))
    return entries, {
        "exact_predecessor_doi": ANNOTATED_PREDECESSOR_DOI,
        "archive": {"bytes": source.stat().st_size, "sha256": sha256(source)},
        "archive_check": check,
        "result": "PASS",
    }


def verify_sibling_release(directory: Path) -> tuple[list[Entry], dict[str, object]]:
    root = directory.resolve(strict=True)
    authority = load_frozen_authority()
    french = authority.get("french_r2")
    if (
        not isinstance(french, dict)
        or french.get("concept_doi") != FRENCH_CONCEPT_DOI
        or french.get("exact_doi") != FRENCH_EXACT_DOI
    ):
        raise RuntimeError("Frozen French R2 authority identity mismatch")
    pinned_rows = french.get("public_files")
    payload_order = french.get("manifest_payload_order")
    if not isinstance(pinned_rows, list) or not isinstance(payload_order, list):
        raise RuntimeError("Frozen French R2 authority is incomplete")
    pins = {
        row.get("name"): row for row in pinned_rows if isinstance(row, dict)
    }
    if set(pins) != set(SIBLING_PUBLIC_NAMES) or payload_order != [
        name for name in SIBLING_PUBLIC_NAMES if name != SIBLING_PUBLIC_NAMES[3]
    ]:
        raise RuntimeError("Frozen French R2 file universe/order mismatch")
    entries: list[Entry] = []
    records: dict[str, dict[str, object]] = {}
    prefix = "fr-10.5281-zenodo.21925876"
    for name in SIBLING_PUBLIC_NAMES:
        source = require_file(root / name, (root,))
        entry = entry_from_file(source, f"{prefix}/{name}", (root,))
        pin = pins[name]
        if (entry.size, entry.digest) != (pin.get("bytes"), pin.get("sha256")):
            raise RuntimeError(f"French R2 frozen public-file pin mismatch: {name}")
        entries.append(entry)
        records[name] = {"bytes": entry.size, "sha256": entry.digest}
    manifest = (root / SIBLING_PUBLIC_NAMES[3]).read_text(encoding="utf-8").splitlines()
    if manifest[:3] != [
        f"# Exact release DOI: {FRENCH_EXACT_DOI}",
        f"# Stable concept DOI: {FRENCH_CONCEPT_DOI}",
        "filename\tbytes\tsha256",
    ]:
        raise RuntimeError("French sibling manifest identity is not the frozen R2 identity")
    payload_lines = manifest[3:]
    if len(payload_lines) != len(payload_order):
        raise RuntimeError("French sibling manifest does not have exactly four payload rows")
    manifest_names: list[str] = []
    for line in payload_lines:
        fields = line.split("\t")
        if len(fields) != 3:
            raise RuntimeError("French sibling manifest row is malformed")
        name, size, digest = fields
        manifest_names.append(name)
        record = records.get(name)
        if not record or (int(size), digest) != (record["bytes"], record["sha256"]):
            raise RuntimeError(f"French sibling manifest mismatch: {name}")
    if manifest_names != payload_order:
        raise RuntimeError("French sibling manifest payload order/universe changed")
    for name in SIBLING_PUBLIC_NAMES:
        if name.endswith(".zip"):
            inspect_zip(
                root / name,
                None,
                scan_content=True,
                scan_absolute_paths=True,
                require_fixed_time=False,
                require_order=False,
            )
    assert_entries_safe((entry for entry in entries if not entry.name.endswith(".zip")), "french-sibling")
    return entries, {
        "exact_doi": FRENCH_EXACT_DOI,
        "concept_doi": FRENCH_CONCEPT_DOI,
        "public_members": records,
        "frozen_authority_sha256": sha256(FROZEN_AUTHORITY_PATH),
        "manifest_payload_order": payload_order,
        "nested_archives_crc_name_symlink_secret_checked": True,
        "nested_archives_absolute_path_scan": "PASS",
        "result": "PASS",
    }


def source_archive_entries(
    publication_root: Path,
    staged_root: Path,
    metadata_entries: list[Entry],
) -> list[Entry]:
    source_root = staged_root / "source"
    entries: list[Entry] = []
    for directory, names in (("english", ANNOTATED_SOURCE_FILES), ("english_direct", DIRECT_SOURCE_FILES)):
        for relative in names:
            entries.append(
                entry_from_file(
                    source_root / directory / relative,
                    f"source/{directory}/{relative}",
                    (staged_root,),
                )
            )
    entries.extend(
        [
            entry_from_file(SCRIPT_ROOT / Path(__file__).name, "build/build_galois_english_r3_two_reader_release.py", (SCRIPT_ROOT,)),
            entry_from_file(SCRIPT_ROOT / "validate_galois_english_direct_projection.py", "build/validate_galois_english_direct_projection.py", (SCRIPT_ROOT,)),
            entry_from_file(SCRIPT_ROOT / "README.md", "build/README.md", (SCRIPT_ROOT,)),
            entry_from_file(FROZEN_AUTHORITY_PATH, "build/GALOIS_R3_FROZEN_AUTHORITY.json", (SCRIPT_ROOT,)),
            entry_from_file(VISUAL_QA_SCHEMA_PATH, "build/GALOIS_R3_VISUAL_QA_RECEIPT_SCHEMA.json", (SCRIPT_ROOT,)),
            entry_from_file(publication_root / "LICENSE", "LICENSE", (publication_root,)),
        ]
    )
    entries.extend(metadata_entries)
    validate_member_set([entry.name for entry in entries], ordered=False)
    return entries


def manifest_bytes(paths: dict[str, Path], exact_doi: str) -> bytes:
    lines = [
        f"Exact DOI: {exact_doi}",
        f"Concept DOI: {CONCEPT_DOI}",
        "SHA256  BYTES  FILENAME",
    ]
    lines.extend(
        f"{sha256(paths[name])}  {paths[name].stat().st_size}  {name}"
        for name in MANIFEST_PAYLOAD_NAMES
    )
    return ("\n".join(lines) + "\n").encode("utf-8")


def compare_outputs(reference: Path, current: dict[str, Path]) -> dict[str, object]:
    reference_children = list(reference.iterdir())
    if (
        {path.name for path in reference_children} != set(PUBLIC_NAMES)
        or any(path.is_symlink() or not path.is_file() for path in reference_children)
    ):
        raise RuntimeError("Comparison directory is not the exact six-file public set")
    records = []
    for name in PUBLIC_NAMES:
        prior = require_file(reference / name, (reference,))
        now = current[name]
        identical = (prior.stat().st_size, sha256(prior)) == (now.stat().st_size, sha256(now))
        if not identical:
            raise RuntimeError(f"Two-build byte identity failed: {name}")
        records.append({"name": name, "bytes": now.stat().st_size, "sha256": sha256(now), "byte_identical": True})
    return {"reference_output_directory": reference.name, "files": records, "all_six_byte_identical": True, "result": "PASS"}


def validate_quarantined_baseline(
    baseline_build: Path,
    exact_doi: str,
    version: str,
    tag: str,
    publication_date: str,
) -> tuple[Path, dict[str, object]]:
    if baseline_build.is_symlink():
        raise ValueError("Baseline build directory may not be a symlink")
    baseline_build = baseline_build.resolve(strict=True)
    if not baseline_build.is_dir():
        raise NotADirectoryError(baseline_build)
    candidate = (baseline_build / "comparison-baseline").resolve(strict=True)
    receipt_path = baseline_build / "R3_RELEASE_BUILD_RECEIPT.json"
    _source, raw, receipt = read_json_object(
        receipt_path, baseline_build, "quarantined baseline build receipt"
    )
    expected_identity = {
        "exact_doi": exact_doi,
        "concept_doi": CONCEPT_DOI,
        "version": version,
        "tag": tag,
        "publication_date": publication_date,
        "annotated_predecessor_exact_doi": ANNOTATED_PREDECESSOR_DOI,
    }
    if (
        receipt.get("schema_version") != 1
        or receipt.get("result") != "BASELINE_QUARANTINED_SECOND_BUILD_REQUIRED"
        or receipt.get("publication_authoritative") is not False
        or receipt.get("identity") != expected_identity
    ):
        raise RuntimeError("Baseline receipt is not an exact quarantined identity gate")
    rows = receipt.get("public_files")
    if not isinstance(rows, list) or [row.get("name") for row in rows if isinstance(row, dict)] != list(PUBLIC_NAMES):
        raise RuntimeError("Baseline receipt public-file universe is malformed")
    row_map = {row["name"]: row for row in rows}
    for name in PUBLIC_NAMES:
        source = require_file(candidate / name, (candidate,))
        if (row_map[name].get("bytes"), row_map[name].get("sha256")) != (
            source.stat().st_size,
            sha256(source),
        ):
            raise RuntimeError(f"Baseline receipt/file binding failed: {name}")
    return candidate, {
        "baseline_build_directory": baseline_build.name,
        "receipt": {
            "name": receipt_path.name,
            "bytes": len(raw),
            "sha256": sha256_bytes(raw),
        },
        "publication_authoritative": False,
        "result": "PASS",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=DEFAULT_PUBLICATION_ROOT)
    parser.add_argument("--exact-doi", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--publication-date", required=True)
    parser.add_argument("--build-directory", required=True)
    parser.add_argument("--output-directory")
    parser.add_argument("--sibling-release-directory", type=Path, default=DEFAULT_SIBLING_RELEASE)
    parser.add_argument("--predecessor-evidence-zip", type=Path, default=DEFAULT_PREDECESSOR_EVIDENCE)
    parser.add_argument("--direct-qa-receipt", type=Path)
    parser.add_argument("--annotated-qa-receipt", type=Path)
    parser.add_argument("--reservation-identity-receipt", type=Path)
    parser.add_argument("--rendered-metadata-directory", type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--reader-preflight", action="store_true")
    mode.add_argument("--establish-comparison-baseline", action="store_true")
    mode.add_argument("--compare-to-baseline-build-directory")
    args = parser.parse_args()

    validate_identity(args.exact_doi, args.version, args.tag, args.publication_date)
    root = args.root.resolve(strict=True)
    if not root.is_dir():
        raise NotADirectoryError(root)
    build_name = validate_leaf(args.build_directory, "--build-directory")
    build = root / "build" / build_name
    output: Path | None = None
    reference: Path | None = None
    baseline_gate: dict[str, object] | None = None
    reservation: dict[str, object] | None = None
    reservation_entry: Entry | None = None
    metadata_entries: list[Entry] | None = None
    metadata: dict[str, object] | None = None
    if args.reader_preflight:
        if any(
            (
                args.output_directory,
                args.direct_qa_receipt,
                args.annotated_qa_receipt,
                args.reservation_identity_receipt,
                args.rendered_metadata_directory,
            )
        ):
            parser.error("reader preflight takes no full-build output, QA, reservation, or metadata inputs")
    else:
        if not all(
            (
                args.direct_qa_receipt,
                args.annotated_qa_receipt,
                args.reservation_identity_receipt,
                args.rendered_metadata_directory,
            )
        ):
            parser.error(
                "full builds require two QA receipts, a reservation identity receipt, "
                "and a rendered metadata directory"
            )
        direct_qa_path = args.direct_qa_receipt.resolve(strict=True)
        annotated_qa_path = args.annotated_qa_receipt.resolve(strict=True)
        if direct_qa_path == annotated_qa_path:
            raise ValueError("Direct and annotated visual QA receipts must be distinct files")
        reservation, reservation_entry = validate_reservation_identity(
            args.reservation_identity_receipt,
            args.exact_doi,
            args.version,
            args.tag,
            args.publication_date,
        )
        metadata_entries, metadata = validate_rendered_metadata(
            args.rendered_metadata_directory,
            args.exact_doi,
            args.version,
            args.tag,
            args.publication_date,
        )
        if args.establish_comparison_baseline:
            if args.output_directory:
                parser.error("a quarantined baseline does not accept --output-directory")
        else:
            if not args.output_directory:
                parser.error("a verified comparison build requires --output-directory")
            output_name = validate_leaf(args.output_directory, "--output-directory")
            output = root / output_name
            reference_name = validate_leaf(
                args.compare_to_baseline_build_directory,
                "--compare-to-baseline-build-directory",
            )
            if reference_name.casefold() == build_name.casefold():
                raise ValueError("Baseline and current build-directory names must differ")
            reference, baseline_gate = validate_quarantined_baseline(
                root / "build" / reference_name,
                args.exact_doi,
                args.version,
                args.tag,
                args.publication_date,
            )

    if build.exists() or (output is not None and output.exists()):
        raise FileExistsError("Build and output directories must be fresh")
    claim_directory(build, root)
    staged_root, original_entries = stage_sources(root, build, args.exact_doi)

    direct_pdf, direct_fls, direct_compile = run_latex(
        staged_root / "source" / "english_direct",
        DIRECT_MASTER,
        build / "pdf-build" / "direct",
    )
    annotated_pdf, annotated_fls, annotated_compile = run_latex(
        staged_root / "source" / "english",
        ANNOTATED_MASTER,
        build / "pdf-build" / "annotated",
    )
    assert_entries_unchanged(original_entries)

    projection = validate_projection(
        staged_root,
        pdf=direct_pdf,
        fls=direct_fls,
        exact_doi=args.exact_doi,
    )
    annotated_input_graph = inspect_reader_work_input_graph(
        annotated_fls,
        staged_root / "source" / "english",
        staged_root / "source" / "english",
        "annotated",
        pdf=annotated_pdf,
    )
    direct_input_graph = projection["compiled_input_graph"]
    if (
        not isinstance(direct_input_graph, dict)
        or direct_input_graph.get("authority_work_set_sha256")
        != annotated_input_graph["authority_work_set_sha256"]
    ):
        raise RuntimeError("The two readers did not compile from the same frozen work authority")
    annotated_structural = inspect_annotated_pdf(annotated_pdf, args.exact_doi)
    if sha256(direct_pdf) == sha256(annotated_pdf):
        raise RuntimeError("The direct and annotated readers unexpectedly have identical bytes")
    assert_entries_safe(
        [
            entry_from_file(direct_pdf, DIRECT_READER_NAME, (build,)),
            entry_from_file(annotated_pdf, ANNOTATED_READER_NAME, (build,)),
        ],
        "reader-pdfs",
    )

    structural_dir = build / "reader-qa"
    structural_dir.mkdir()
    projection_path = structural_dir / "DIRECT_SOURCE_PROJECTION_VALIDATION.json"
    annotated_path = structural_dir / "ANNOTATED_READER_STRUCTURAL_VALIDATION.json"
    write_new(projection_path, json_bytes(projection), build)
    annotated_validation = {
        "schema_version": 1,
        "reader_role": "GPT-annotated English reader",
        "reader": annotated_structural,
        "compiled_input_graph": annotated_input_graph,
        "same_frozen_work_authority_as_direct": True,
        "result": "PASS",
    }
    annotated_build_validation = {**annotated_validation, "compile": annotated_compile}
    write_new(
        annotated_path,
        json_bytes(annotated_build_validation),
        build,
    )

    if args.reader_preflight:
        preflight = build / "reader-preflight"
        preflight.mkdir()
        copy_new(direct_pdf, preflight / DIRECT_READER_NAME, build)
        copy_new(annotated_pdf, preflight / ANNOTATED_READER_NAME, build)
        receipt = {
            "schema_version": 1,
            "result": "PASS_READERS_READY_FOR_ALL_PAGE_VISUAL_QA",
            "identity": {
                "exact_doi": args.exact_doi,
                "concept_doi": CONCEPT_DOI,
                "version": args.version,
                "tag": args.tag,
                "publication_date": args.publication_date,
            },
            "direct_reader": projection["pdf"],
            "annotated_reader": annotated_structural,
            "direct_compile": direct_compile,
            "annotated_compile": annotated_compile,
            "direct_shared_input_graph": projection["compiled_input_graph"],
            "annotated_shared_input_graph": annotated_input_graph,
            "next": "Render and inspect every page; create separate JSON QA receipts binding these exact hashes; then run two fresh full package builds.",
        }
        payload = json_bytes(receipt)
        write_new(build / "R3_READER_PREFLIGHT_RECEIPT.json", payload, build)
        print(payload.decode("utf-8"), end="")
        return 0

    assert args.direct_qa_receipt and args.annotated_qa_receipt
    assert reservation is not None and reservation_entry is not None
    assert metadata_entries is not None and metadata is not None
    direct_visual = bind_visual_receipt(
        args.direct_qa_receipt,
        projection["pdf"],
        "source-faithful English reader",
        args.exact_doi,
    )
    annotated_visual = bind_visual_receipt(
        args.annotated_qa_receipt,
        annotated_structural,
        "GPT-annotated English reader",
        args.exact_doi,
    )
    candidate = build / (
        "comparison-baseline"
        if args.establish_comparison_baseline
        else "comparison-candidate"
    )
    claim_directory(candidate, root)
    public_paths = {
        DIRECT_READER_NAME: candidate / DIRECT_READER_NAME,
        ANNOTATED_READER_NAME: candidate / ANNOTATED_READER_NAME,
        SOURCE_ZIP_NAME: candidate / SOURCE_ZIP_NAME,
        EVIDENCE_ZIP_NAME: candidate / EVIDENCE_ZIP_NAME,
        MANIFEST_NAME: candidate / MANIFEST_NAME,
        OTHER_TRANSLATIONS_NAME: candidate / OTHER_TRANSLATIONS_NAME,
    }
    copy_new(direct_pdf, public_paths[DIRECT_READER_NAME], root)
    copy_new(annotated_pdf, public_paths[ANNOTATED_READER_NAME], root)

    source_entries = source_archive_entries(
        root,
        staged_root,
        metadata_entries,
    )
    assert_entries_safe(source_entries, "editable-sources")
    write_zip(public_paths[SOURCE_ZIP_NAME], root, source_entries)
    source_check = inspect_zip(
        public_paths[SOURCE_ZIP_NAME],
        {entry.name: (entry.size, entry.digest) for entry in source_entries},
        scan_content=True,
        scan_absolute_paths=True,
        require_fixed_time=True,
        require_order=True,
    )

    evidence_entries, predecessor_evidence = load_predecessor_evidence(args.predecessor_evidence_zip)
    new_evidence = [
        entry_from_data(json_bytes(projection), "evidence/r3/DIRECT_SOURCE_PROJECTION_VALIDATION.json"),
        entry_from_data(json_bytes(annotated_validation), "evidence/r3/ANNOTATED_READER_STRUCTURAL_VALIDATION.json"),
        entry_from_data(json_bytes(direct_visual), "evidence/r3/DIRECT_READER_ALL_PAGE_QA.json"),
        entry_from_data(json_bytes(annotated_visual), "evidence/r3/ANNOTATED_READER_ALL_PAGE_QA.json"),
        entry_from_file(
            args.direct_qa_receipt,
            "evidence/r3/DIRECT_READER_ALL_PAGE_QA_SOURCE.json",
            (args.direct_qa_receipt.parent.resolve(strict=True),),
        ),
        entry_from_file(
            args.annotated_qa_receipt,
            "evidence/r3/ANNOTATED_READER_ALL_PAGE_QA_SOURCE.json",
            (args.annotated_qa_receipt.parent.resolve(strict=True),),
        ),
        reservation_entry,
        entry_from_file(
            FROZEN_AUTHORITY_PATH,
            "evidence/r3/GALOIS_R3_FROZEN_AUTHORITY.json",
            (SCRIPT_ROOT,),
        ),
        entry_from_data(
            json_bytes(metadata),
            "evidence/r3/R3_RENDERED_METADATA_VALIDATION.json",
        ),
        entry_from_data(
            json_bytes(
                {
                    "schema_version": 1,
                    "exact_doi": args.exact_doi,
                    "concept_doi": CONCEPT_DOI,
                    "annotated_predecessor": {
                        "exact_doi": ANNOTATED_PREDECESSOR_DOI,
                        "reader_sha256": ANNOTATED_PREDECESSOR_READER_SHA256,
                        "preserved": True,
                    },
                    "version": args.version,
                    "tag": args.tag,
                    "publication_date": args.publication_date,
                    "result": "PASS",
                }
            ),
            "evidence/r3/R3_RELEASE_IDENTITY_AND_PREDECESSOR_PIN.json",
        ),
    ]
    evidence_entries.extend(new_evidence)
    validate_member_set([entry.name for entry in evidence_entries], ordered=False)
    assert_entries_safe(evidence_entries, "evidence")
    write_zip(public_paths[EVIDENCE_ZIP_NAME], root, evidence_entries)
    evidence_check = inspect_zip(
        public_paths[EVIDENCE_ZIP_NAME],
        {entry.name: (entry.size, entry.digest) for entry in evidence_entries},
        scan_content=True,
        scan_absolute_paths=True,
        require_fixed_time=True,
        require_order=True,
    )

    sibling_entries, sibling = verify_sibling_release(args.sibling_release_directory)
    write_zip(public_paths[OTHER_TRANSLATIONS_NAME], root, sibling_entries)
    sibling_check = inspect_zip(
        public_paths[OTHER_TRANSLATIONS_NAME],
        {entry.name: (entry.size, entry.digest) for entry in sibling_entries},
        scan_content=True,
        scan_absolute_paths=True,
        require_fixed_time=True,
        require_order=True,
    )

    write_new(
        public_paths[MANIFEST_NAME],
        manifest_bytes(public_paths, args.exact_doi),
        root,
    )
    if public_paths[MANIFEST_NAME].read_bytes() != manifest_bytes(public_paths, args.exact_doi):
        raise RuntimeError("Manifest canonical-byte validation failed")
    assert_entries_safe(
        [
            entry_from_file(public_paths[name], name, (candidate,))
            for name in PUBLIC_NAMES
            if not name.endswith(".zip")
        ],
        "public-files",
    )
    candidate_children = list(candidate.iterdir())
    if (
        {path.name for path in candidate_children} != set(PUBLIC_NAMES)
        or any(path.is_symlink() or not path.is_file() for path in candidate_children)
    ):
        raise RuntimeError("Candidate is not the exact six-file public inventory")

    if args.establish_comparison_baseline:
        comparison = {
            "all_six_byte_identical": False,
            "publication_authoritative": False,
            "quarantined_under_build_directory": True,
            "result": "BASELINE_QUARANTINED_SECOND_BUILD_REQUIRED",
        }
        result = "BASELINE_QUARANTINED_SECOND_BUILD_REQUIRED"
        publication_authoritative = False
        authoritative_paths = public_paths
    else:
        assert reference is not None and output is not None and baseline_gate is not None
        comparison = compare_outputs(reference, public_paths)
        if comparison.get("all_six_byte_identical") is not True:
            raise RuntimeError("Verified comparison did not close byte identity")
        claim_directory(output, root)
        authoritative_paths = {name: output / name for name in PUBLIC_NAMES}
        for name in PUBLIC_NAMES:
            copy_new(public_paths[name], authoritative_paths[name], root)
        output_children = list(output.iterdir())
        if (
            {path.name for path in output_children} != set(PUBLIC_NAMES)
            or any(path.is_symlink() or not path.is_file() for path in output_children)
        ):
            raise RuntimeError("Verified output is not the exact six-file public inventory")
        compare_outputs(candidate, authoritative_paths)
        result = "PASS"
        publication_authoritative = True
    receipt = {
        "schema_version": 1,
        "result": result,
        "publication_authoritative": publication_authoritative,
        "publication_output_directory": output.name if publication_authoritative else None,
        "quarantined_candidate_directory": candidate.name,
        "identity": {
            "exact_doi": args.exact_doi,
            "concept_doi": CONCEPT_DOI,
            "version": args.version,
            "tag": args.tag,
            "publication_date": args.publication_date,
            "annotated_predecessor_exact_doi": ANNOTATED_PREDECESSOR_DOI,
        },
        "non_destructive_policy": {
            "fresh_build_directory": True,
            "fresh_output_directory": publication_authoritative,
            "recursive_cleanup": False,
            "git_or_remote_mutation": False,
            "credential_access": False,
        },
        "public_files": [
            {
                "name": name,
                "bytes": authoritative_paths[name].stat().st_size,
                "sha256": sha256(authoritative_paths[name]),
            }
            for name in PUBLIC_NAMES
        ],
        "direct_reader": {
            "projection": projection,
            "compile": direct_compile,
            "all_page_qa_binding": direct_visual,
        },
        "annotated_reader": {
            "structure": annotated_structural,
            "compiled_input_graph": annotated_input_graph,
            "compile": annotated_compile,
            "all_page_qa_binding": annotated_visual,
        },
        "same_corpus_compiled_input_graph_proof": {
            "direct": projection["compiled_input_graph"],
            "annotated": annotated_input_graph,
            "authority_work_set_sha256": annotated_input_graph[
                "authority_work_set_sha256"
            ],
            "all_eleven_resolved_authority_hashes_identical": True,
            "result": "PASS",
        },
        "archives": {
            SOURCE_ZIP_NAME: source_check,
            EVIDENCE_ZIP_NAME: evidence_check,
            OTHER_TRANSLATIONS_NAME: sibling_check,
        },
        "reservation_identity": reservation,
        "rendered_metadata": metadata,
        "baseline_receipt_gate": baseline_gate,
        "predecessor_evidence": predecessor_evidence,
        "french_sibling": sibling,
        "manifest": {
            "payload_rows": 5,
            "self_hashing": False,
            "canonical_header": True,
            "result": "PASS",
        },
        "two_build_byte_identity": comparison,
        "exact_public_inventory": list(PUBLIC_NAMES),
    }
    payload = json_bytes(receipt)
    write_new(build / "R3_RELEASE_BUILD_RECEIPT.json", payload, build)
    print(payload.decode("utf-8"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
