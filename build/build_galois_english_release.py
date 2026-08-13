#!/usr/bin/env python3
"""Build a non-destructive, deterministic, public-safe Galois English release."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import stat
import subprocess
import unicodedata
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import BinaryIO, Iterable


WORKSPACE = Path(__file__).resolve().parent
DEFAULT_ROOT = WORKSPACE / "galois-en-publication"
DEFAULT_FRENCH_ROOT = WORKSPACE / "galois-fr-publication"
DEFAULT_FRENCH_ARTIFACT_DIRECTORY = WORKSPACE / "galois_zenodo_artifacts"

FIXED_TIME = (2026, 8, 14, 0, 0, 0)
FRENCH_FIXED_TIME = (1980, 1, 1, 0, 0, 0)
ZIP_COMPRESSION_LEVEL = 9
STREAM_BLOCK_SIZE = 1024 * 1024
SCAN_OVERLAP = 4096

ENGLISH_EXACT_DOI = "10.5281/zenodo.21924302"
ENGLISH_CONCEPT_DOI = "10.5281/zenodo.21924301"
FRENCH_EXACT_DOI = "10.5281/zenodo.21923857"
FRENCH_CONCEPT_DOI = "10.5281/zenodo.21923856"
FRENCH_ARCHIVE_PREFIX = "fr-10.5281-zenodo.21923857"

READER_NAME = "00_GALOIS_1897_EN_CURRENT_LINKED_READER.pdf"
SOURCE_ZIP_NAME = "01_GALOIS_1897_EN_EDITABLE_SOURCES.zip"
EVIDENCE_ZIP_NAME = "02_GALOIS_1897_EN_EVIDENCE_AND_PROVENANCE.zip"
MANIFEST_NAME = "03_GALOIS_1897_EN_SHA256_MANIFEST.txt"
OTHER_TRANSLATIONS_NAME = "OTHER_TRANSLATIONS.zip"
RELEASE_RECEIPT_NAME = "RELEASE_BUILD_RECEIPT.json"
PUBLIC_FILE_NAMES = (
    READER_NAME,
    SOURCE_ZIP_NAME,
    EVIDENCE_ZIP_NAME,
    MANIFEST_NAME,
    OTHER_TRANSLATIONS_NAME,
)


# Every packaged English source file is named here. New source files must be reviewed
# and deliberately added; filesystem discovery is never used to populate an archive.
SOURCE_FIGURES = (
    "figures/PDF007_L0006_PUBLISHER_DEVICE.png",
    "figures/PDF019_L0018_PORTRAIT_PLATE.png",
    "figures/PDF021_L0020_PORTRAIT_PLATE_DEGRADED.png",
    "figures/PDF024_L0023_MARGIN_X_ENHANCED.png",
    "figures/PDF029_L0028_END_ORNAMENT_ENHANCED.png",
    "figures/PDF030_L0029_TITLE_MARK_ENHANCED.png",
    "figures/PDF052_L0051_TERMINAL_ORNAMENT_ENHANCED.png",
    "figures/PDF052_L0051_TERMINAL_ORNAMENT_RAW.png",
    "figures/PDF093_L0092_PRINTER_JOB_NUMBER_ENHANCED.png",
)
SOURCE_WORKS = (
    "tex/works/GAL1897_W01_PRELIMS.tex",
    "tex/works/GAL1897_W02_INTRODUCTION.tex",
    "tex/works/GAL1897_W03_CONTINUED_FRACTIONS.tex",
    "tex/works/GAL1897_W04_NOTES_ANALYSIS.tex",
    "tex/works/GAL1897_W05_ALGEBRAIC_RESOLUTION_ANALYSIS.tex",
    "tex/works/GAL1897_W06_NUMERICAL_EQUATIONS.tex",
    "tex/works/GAL1897_W07_NUMBER_THEORY.tex",
    "tex/works/GAL1897_W08_CHEVALIER_LETTER.tex",
    "tex/works/GAL1897_W09_RADICALS_MEMOIR.tex",
    "tex/works/GAL1897_W10_PRIMITIVE_EQUATIONS.tex",
    "tex/works/GAL1897_W11_BACKMATTER.tex",
)
SOURCE_FILE_ALLOWLIST = (
    "GAL1897_EN_MODERN_READER.tex",
    "STYLE_GUIDE.md",
    *SOURCE_FIGURES,
    *(f"tex/pages/PDF{number:03d}.tex" for number in range(62, 92)),
    *SOURCE_WORKS,
    *(f"tex/wrappers/W{number:02d}.tex" for number in range(1, 12)),
)
SOURCE_DISCOVERY_EXCLUSIONS = ("$out/", "work/", "__pycache__/")
ROOT_METADATA_ALLOWLIST = (
    "README.md",
    "LICENSE",
    "CITATION.cff",
    ".zenodo.json",
    "BUILD_INSTRUCTIONS.md",
)
SOURCE_SIDECAR_ALLOWLIST = (
    "evidence/SOURCE_AUTHORITY.json",
    "evidence/DATACITE_RELATIONS.json",
    "qa/galois_english_pdf_visual_inspection.schema.json",
    "qa/galois_english_pdf_visual_inspection.template.json",
)
BUILD_SCRIPT_ALLOWLIST = (
    "build_galois_translation_ledgers.py",
    "validate_galois_translation_structure.py",
    "qa_galois_english_reader.py",
    "qa_galois_english_render.py",
    "build_galois_english_release.py",
)


# Exact, public-safe evidence inputs. Deliberately absent: release_metadata_draft,
# pre-patch/incident material, duplicate downloads, internal durable workflow/state,
# task/action ledgers, credential helpers, and RETURN_TO_CODEX workflow logs.
EVIDENCE_EXACT_ALLOWLIST = (
    "evidence/alignment_fragments/W05_W08.tsv",
    "evidence/coverage_fragments/W05_W08.tsv",
    "evidence/DATACITE_RELATIONS.json",
    "evidence/EN_FR_ALIGNMENT.tsv",
    "evidence/ENGLISH_COVERAGE.tsv",
    "evidence/fragments/AUDIT_W05_W08.md",
    "evidence/fragments/AUDIT_W09_W11.md",
    "evidence/fragments/FINAL_REAUDIT_W01_W04_W09_W11.md",
    "evidence/GPT_CRITICAL_CALLOUTS.tsv",
    "evidence/POST_P13_INTEGRATION_SUMMARY.json",
    "evidence/POST_P13_TASK_DISPOSITIONS.tsv",
    "evidence/QA_REPORT.md",
    "evidence/QA_STATE.json",
    "evidence/RELEASE_SURFACE.md",
    "evidence/SEMANTIC_AUDIT_CLOSURE_POST_P13.md",
    "evidence/SOURCE_AUTHORITY.json",
    "evidence/STRUCTURAL_VALIDATION_POST_P13.json",
    "evidence/TRANSLATION_LEDGER_BUILD.json",
    "evidence/UNRESOLVED_ITEMS.tsv",
)
CRITICAL_BASELINE_ALLOWLIST = (
    "source/critical_baseline/DEFERRED_AUDIT_REGISTER.csv",
    "source/critical_baseline/ERRATA_AND_UNRESOLVED_LEDGER.csv",
    "source/critical_baseline/GPT_EDITION_HANDOFF.md",
    "source/critical_baseline/GPT_EDITION_NOTES_FROM_P00-P11.md",
    "source/critical_baseline/PRINTED_AND_SOURCE_ERRORS.csv",
    "source/critical_baseline/PRINTED_AND_SOURCE_ERRORS.md",
    "source/critical_baseline/WITNESS_VARIANTS.csv",
    "source/critical_baseline/WITNESS_VARIANTS.md",
)
WEB_RETURN_SUBSTANTIVE_ALLOWLIST = (
    "evidence/web_post_p13_return/BIBLIOGRAPHIC_PRIOR_NOTICE_MATRIX.csv",
    "evidence/web_post_p13_return/COLD_AUDIT_CHECKS.json",
    "evidence/web_post_p13_return/CRITICAL_ERRATA_CATALOGUE.csv",
    "evidence/web_post_p13_return/DEPENDENCY_PROPAGATION_EDGES.csv",
    "evidence/web_post_p13_return/"
    "GAL1897_CUMULATIVE_P00-P13R_POST_P13_GPT_CRITICAL_EDITION_21_TASKS.zip.sha256",
    "evidence/web_post_p13_return/GAL1897_GPT_CRITICAL_EDITION.md",
    "evidence/web_post_p13_return/GAL1897_GPT_CRITICAL_EDITION.pdf",
    "evidence/web_post_p13_return/"
    "GAL1897_ONE_CLICK_READER_DIPLOMATIC_PLUS_GPT_CRITICAL.pdf",
    "evidence/web_post_p13_return/"
    "GAL1897_POST_P13_GPT_CRITICAL_EDITION_21_TASKS_PACKAGE_RECEIPT.json",
    "evidence/web_post_p13_return/MASTER_21_TASK_LEDGER.csv",
    "evidence/web_post_p13_return/OPEN_AFTER_21_TASKS.csv",
    "evidence/web_post_p13_return/SEARCH_QUERY_LEDGER.csv",
    "evidence/web_post_p13_return/WEB_RESEARCH_PROVENANCE.md",
    "evidence/web_post_p13_return/WEB_SOURCE_EVIDENCE.csv",
)
PUBLIC_PROJECTION_SPECS = (
    (
        "evidence/BUILD_ENVIRONMENT.json",
        "evidence/public_receipts/BUILD_ENVIRONMENT_PUBLIC.json",
        "json",
    ),
    (
        "evidence/READER_STRUCTURAL_QA_POST_P13.json",
        "evidence/public_receipts/READER_STRUCTURAL_QA_POST_P13_PUBLIC.json",
        "json",
    ),
    (
        "evidence/READER_MECHANICAL_RENDER_QA_POST_P13.json",
        "evidence/public_receipts/READER_MECHANICAL_RENDER_QA_POST_P13_PUBLIC.json",
        "json",
    ),
    (
        "evidence/READER_VISUAL_INSPECTION_POST_P13.json",
        "evidence/public_receipts/READER_VISUAL_INSPECTION_POST_P13_PUBLIC.json",
        "visual_receipt",
    ),
    (
        "evidence/web_post_p13_return/INDIVIDUAL_DOWNLOAD_VALIDATION_RECEIPT.json",
        "evidence/web_post_p13_return/"
        "INDIVIDUAL_DOWNLOAD_VALIDATION_PUBLIC_RECEIPT.json",
        "web_receipt",
    ),
)
PREPACKAGE_RECEIPT_ARCNAME = (
    "evidence/public_receipts/PREPACKAGE_VALIDATION_RECEIPT.json"
)


# Frozen public French r1 package. The artifact hashes are the published release
# pins; the four repository metadata files are separately frozen here so mutable
# live metadata can never be silently nested under the r1 DOI directory.
FRENCH_PUBLIC_PINS = (
    (
        "00_GALOIS_1897_FR_CURRENT_LINKED_READER.pdf",
        "artifact",
        3_859_917,
        "F62D37396E04C2FC04680125E8600206FD82FA82ACE9689FF439BF30E786895A",
    ),
    (
        "01_GALOIS_1897_FR_EDITABLE_SOURCES.zip",
        "artifact",
        6_452_408,
        "E990DA8591F64FF01891F6ED0CC36FB9FCBFEA6B25995C19E526492D7EC066A8",
    ),
    (
        "02_GALOIS_1897_FR_EVIDENCE_AND_PROVENANCE.zip",
        "artifact",
        283_491_687,
        "A0BDEFDBD8757561286B0C43EA3597DE0B2DD90FE66B54A6CF5F9BEE92404CD9",
    ),
    (
        "03_GALOIS_1897_FR_SHA256_MANIFEST.txt",
        "artifact",
        463,
        "E1F334DE24DC6B9E57C1334B9FAA82470CA3D737E0A9A642C7A9CF1573971114",
    ),
    (
        "README.md",
        "metadata",
        3_283,
        "3A4FA666EE76E96B7679361D4FA0FB4618E5E8A97E5589E1BB0A2E5BEA672FB3",
    ),
    (
        "LICENSE",
        "metadata",
        1_166,
        "13627E4B86A1C77729845D2AE622491C59B5E695C1079374685CBD84C29D0FD4",
    ),
    (
        "CITATION.cff",
        "metadata",
        992,
        "8799C6F69D00CA7A09994FA52F1CB5EA04FBE217B3165D1693B9F1BC7C18232D",
    ),
    (
        ".zenodo.json",
        "metadata",
        2_599,
        "C5D153C289E6A918CF6CDC824A4EA173E1E2772E14FAACE0CD75E51E0167037B",
    ),
)


FORBIDDEN_PUBLIC_BASENAMES = {
    "DURABLE_GALOIS_ENGLISH_DOI_WORKFLOW.md".casefold(),
    "GALOIS_ENGLISH_STATE.json".casefold(),
    "GALOIS_ENGLISH_ACTION_LEDGER.jsonl".casefold(),
    "GALOIS_ENGLISH_DECISIONS.md".casefold(),
    "STRUCTURAL_VALIDATION_PREPATCH.json".casefold(),
    ("git" + "hub_askpass.cmd").casefold(),
}
FORBIDDEN_PUBLIC_PARTS = {
    "$out".casefold(),
    "__pycache__".casefold(),
    "release_metadata_draft".casefold(),
}
SUSPICIOUS_MEMBER_BASENAMES = {
    ".env".casefold(),
    ("credentials" + ".json").casefold(),
    ("git" + "hub_askpass.cmd").casefold(),
    ("zenodo" + "_token.txt").casefold(),
}


# Pattern fragments are deliberately separated so the scanner source can itself be
# distributed without looking like a credential. Match labels, never values, are
# reported on failure.
ABSOLUTE_PATH_PATTERNS = (
    (
        "windows_absolute_path",
        re.compile(rb"(?i)(?<![A-Za-z0-9+.-])[A-Z]:[\\/]"),
    ),
    (
        "windows_unc_path",
        re.compile(rb"(?<![\\])\\\\[A-Za-z0-9._$-]+[\\/][A-Za-z0-9._$-]+"),
    ),
    (
        "unix_private_absolute_path",
        re.compile(rb"(?i)(?<![A-Za-z0-9])/(?:home|Users|tmp|var/tmp)/"),
    ),
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
    (
        "github_fine_grained_token",
        re.compile(rb"github" + rb"_pat_[A-Za-z0-9_]{20,}"),
    ),
    (
        "github_classic_token",
        re.compile(rb"gh" + rb"[pousr]_[A-Za-z0-9]{20,}"),
    ),
    (
        "bearer_token",
        re.compile(
            rb"(?i)Authorization\s*:\s*Bearer\s+[A-Za-z0-9._~+/=-]{20,}"
        ),
    ),
    (
        "assigned_secret",
        re.compile(
            rb"(?i)\b(?:access[_-]?" + rb"token|api[_-]?key|client[_-]?"
            rb"secret|pass" + rb"word|passwd)[\"']?\s*[=:]\s*[\"']?"
            rb"[A-Za-z0-9._~+/=-]{12,}"
        ),
    ),
    ("aws_access_key", re.compile(rb"(?<![A-Z0-9])AKIA[A-Z0-9]{16}(?![A-Z0-9])")),
    (
        "private_key_material",
        re.compile(
            rb"-----BEGIN " + rb"(?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
        ),
    ),
    (
        "credential_file_reference",
        re.compile(
            rb"(?i)(?:^|[\\/])(?:git" + rb"hub_askpass\.cmd|credentials\.json|"
            rb"zenodo[_-]?token(?:\.txt)?)"
        ),
    ),
)

_WINDOWS_PATH_TEXT = re.compile(
    r"(?i)(?<![A-Za-z0-9+.-])[A-Z]:[\\/][^\s`\"'<>]+"
)
_UNIX_PATH_TEXT = re.compile(
    r"(?i)(?<![A-Za-z0-9])/(?:home|Users|tmp|var/tmp)/[^\s`\"'<>]+"
)
_FILE_URI_TEXT = re.compile(r"(?i)file:" + r"///[^\s`\"'<>]+")
_SAFE_LEAF = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_DOS_RESERVED = re.compile(r"(?i)(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?\Z")
OPAQUE_SCAN_SUFFIXES = {
    ".zip",
}
STRONG_BINARY_SCAN_SUFFIXES = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".jp2",
    ".tif",
    ".tiff",
}


@dataclass(frozen=True)
class PreparedEntry:
    arcname: str
    size: int
    digest: str
    source: Path | None = None
    data: bytes | None = None

    def public_record(self) -> dict[str, object]:
        return {"name": self.arcname, "bytes": self.size, "sha256": self.digest}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(STREAM_BLOCK_SIZE), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")


def ensure_within(path: Path, root: Path) -> None:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=True))
    except ValueError as error:
        raise ValueError(f"Path escapes declared root: {path}") from error


def require_regular_file(path: Path, allowed_roots: Iterable[Path]) -> Path:
    if path.is_symlink():
        raise ValueError(f"Symlink inputs are prohibited: {path}")
    resolved = path.resolve(strict=True)
    if not resolved.is_file():
        raise FileNotFoundError(f"Required regular file is missing: {path}")
    if not any(_is_within(resolved, root) for root in allowed_roots):
        raise ValueError(f"Input is outside its declared roots: {path}")
    return resolved


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root.resolve(strict=True))
        return True
    except ValueError:
        return False


def validate_leaf_name(value: str, option: str) -> str:
    if not _SAFE_LEAF.fullmatch(value) or value in {".", ".."}:
        raise ValueError(
            f"{option} must be one safe, relative directory name: {value!r}"
        )
    if _DOS_RESERVED.fullmatch(value):
        raise ValueError(f"{option} uses a reserved filesystem name: {value!r}")
    return value


def claim_new_directory(path: Path, root: Path) -> None:
    ensure_within(path, root)
    if path.exists():
        raise FileExistsError(f"Refusing to reuse any existing directory: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.mkdir()


def write_new_bytes(path: Path, data: bytes, root: Path) -> None:
    ensure_within(path, root)
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite file: {path}")
    with path.open("xb") as stream:
        stream.write(data)


def validate_member_name(name: str) -> None:
    if not name or "\x00" in name or "\\" in name:
        raise ValueError(f"Unsafe ZIP member name: {name!r}")
    if name.startswith("/") or re.match(r"(?i)^[A-Z]:", name):
        raise ValueError(f"Absolute ZIP member name: {name!r}")
    if any(ord(character) < 32 or ord(character) == 127 for character in name):
        raise ValueError(f"Control character in ZIP member name: {name!r}")
    if unicodedata.normalize("NFC", name) != name:
        raise ValueError(f"Non-NFC ZIP member name: {name!r}")
    parts = name.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError(f"Non-canonical ZIP member name: {name!r}")
    if any(part.endswith((" ", ".")) or _DOS_RESERVED.fullmatch(part) for part in parts):
        raise ValueError(f"Platform-unsafe ZIP member name: {name!r}")
    if PurePosixPath(name).as_posix() != name:
        raise ValueError(f"Non-POSIX ZIP member name: {name!r}")


def reject_internal_public_name(name: str) -> None:
    parts = PurePosixPath(name).parts
    if any(part.casefold() in FORBIDDEN_PUBLIC_PARTS for part in parts):
        raise ValueError(f"Internal workflow path is prohibited from release: {name}")
    if parts[-1].casefold() in FORBIDDEN_PUBLIC_BASENAMES:
        raise ValueError(f"Internal workflow file is prohibited from release: {name}")
    if parts[-1].casefold() in SUSPICIOUS_MEMBER_BASENAMES:
        raise ValueError(f"Credential-like filename is prohibited from release: {name}")
    if parts[-1].casefold().startswith("return_to_codex"):
        raise ValueError(f"Internal return log is prohibited from release: {name}")


def validate_member_set(names: list[str], *, enforce_order: bool) -> None:
    for name in names:
        validate_member_name(name)
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise ValueError(f"Duplicate ZIP member names: {duplicates}")
    normalized: dict[str, str] = {}
    for name in names:
        key = unicodedata.normalize("NFC", name).casefold()
        if key in normalized:
            raise ValueError(
                f"Case/Unicode-colliding ZIP names: {normalized[key]!r}, {name!r}"
            )
        normalized[key] = name
    if enforce_order and names != sorted(names):
        raise ValueError("ZIP members are not in canonical lexical order")


def prepare_file_entry(
    source: Path, arcname: str, allowed_roots: Iterable[Path]
) -> PreparedEntry:
    validate_member_name(arcname)
    reject_internal_public_name(arcname)
    resolved = require_regular_file(source, allowed_roots)
    size = resolved.stat().st_size
    return PreparedEntry(arcname, size, sha256(resolved), source=resolved)


def prepare_data_entry(data: bytes, arcname: str) -> PreparedEntry:
    validate_member_name(arcname)
    reject_internal_public_name(arcname)
    return PreparedEntry(arcname, len(data), sha256_bytes(data), data=data)


def assert_entries_unchanged(entries: Iterable[PreparedEntry]) -> None:
    for entry in entries:
        if entry.source is None:
            continue
        actual_size = entry.source.stat().st_size
        actual_hash = sha256(entry.source)
        if (actual_size, actual_hash) != (entry.size, entry.digest):
            raise RuntimeError(f"Input changed during build: {entry.arcname}")


def entry_fingerprint(entries: Iterable[PreparedEntry]) -> str:
    digest = hashlib.sha256()
    for entry in sorted(entries, key=lambda item: item.arcname):
        digest.update(
            f"{entry.arcname}\t{entry.size}\t{entry.digest}\n".encode("utf-8")
        )
    return digest.hexdigest().upper()


def _scan_chunks(
    chunks: Iterable[bytes], *, include_absolute_paths: bool
) -> tuple[str, ...]:
    patterns = SECRET_PATTERNS + (
        ABSOLUTE_PATH_PATTERNS if include_absolute_paths else ()
    )
    hits: set[str] = set()
    carry = b""
    for chunk in chunks:
        block = carry + chunk
        for label, pattern in patterns:
            if label not in hits and pattern.search(block):
                hits.add(label)
        carry = block[-SCAN_OVERLAP:]
    return tuple(sorted(hits))


def scan_bytes(data: bytes, *, include_absolute_paths: bool = True) -> tuple[str, ...]:
    return _scan_chunks((data,), include_absolute_paths=include_absolute_paths)


def scan_stream(
    stream: BinaryIO, *, include_absolute_paths: bool = True
) -> tuple[str, ...]:
    return _scan_chunks(
        iter(lambda: stream.read(STREAM_BLOCK_SIZE), b""),
        include_absolute_paths=include_absolute_paths,
    )


def content_is_scannable(name: str) -> bool:
    """Return whether raw pattern scanning is meaningful for this payload type."""
    return PurePosixPath(name).suffix.casefold() not in OPAQUE_SCAN_SUFFIXES


def patterns_for_payload(
    name: str, *, include_absolute_paths: bool
) -> tuple[tuple[str, re.Pattern[bytes]], ...]:
    if not content_is_scannable(name):
        return ()
    absolute_patterns = (
        PDF_ABSOLUTE_PATH_PATTERNS
        if PurePosixPath(name).suffix.casefold() in STRONG_BINARY_SCAN_SUFFIXES
        else ABSOLUTE_PATH_PATTERNS
    )
    return SECRET_PATTERNS + (absolute_patterns if include_absolute_paths else ())


def scan_named_stream(
    stream: BinaryIO, name: str, *, include_absolute_paths: bool = True
) -> tuple[str, ...]:
    patterns = patterns_for_payload(name, include_absolute_paths=include_absolute_paths)
    hits: set[str] = set()
    carry = b""
    for chunk in iter(lambda: stream.read(STREAM_BLOCK_SIZE), b""):
        block = carry + chunk
        for label, pattern in patterns:
            if label not in hits and pattern.search(block):
                hits.add(label)
        carry = block[-SCAN_OVERLAP:]
    return tuple(sorted(hits))


def scan_named_bytes(
    data: bytes, name: str, *, include_absolute_paths: bool = True
) -> tuple[str, ...]:
    patterns = patterns_for_payload(name, include_absolute_paths=include_absolute_paths)
    return tuple(sorted(label for label, pattern in patterns if pattern.search(data)))


def assert_public_entries_safe(entries: Iterable[PreparedEntry], context: str) -> int:
    count = 0
    for entry in entries:
        reject_internal_public_name(entry.arcname)
        if entry.data is not None:
            hits = scan_named_bytes(entry.data, entry.arcname)
        else:
            assert entry.source is not None
            with entry.source.open("rb") as stream:
                hits = scan_named_stream(stream, entry.arcname)
        if hits:
            raise RuntimeError(
                f"Public-safety scan failed in {context}/{entry.arcname}: "
                + ", ".join(hits)
            )
        count += 1
    return count


def audit_source_inventory(english: Path) -> None:
    allowed = set(SOURCE_FILE_ALLOWLIST)
    missing = sorted(name for name in allowed if not (english / name).is_file())
    if missing:
        raise FileNotFoundError("Missing allowlisted English sources: " + "; ".join(missing))
    unexpected: list[str] = []
    for path in english.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(english).as_posix()
        if relative in allowed:
            continue
        if any(relative.startswith(prefix) for prefix in SOURCE_DISCOVERY_EXCLUSIONS):
            continue
        unexpected.append(relative)
    if unexpected:
        raise RuntimeError(
            "Unexpected English source files require explicit allowlist review: "
            + "; ".join(sorted(unexpected))
        )


def validate_qa_receipts(root: Path) -> dict[str, object]:
    def read_object(relative: str) -> dict[str, object]:
        value = json.loads((root / relative).read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise RuntimeError(f"Required QA receipt is not a JSON object: {relative}")
        return value

    structural = read_object("evidence/STRUCTURAL_VALIDATION_POST_P13.json")
    reader = read_object("evidence/READER_STRUCTURAL_QA_POST_P13.json")
    mechanical = read_object("evidence/READER_MECHANICAL_RENDER_QA_POST_P13.json")
    visual = read_object("evidence/READER_VISUAL_INSPECTION_POST_P13.json")
    qa_state = read_object("evidence/QA_STATE.json")
    failures: list[str] = []
    if structural.get("pass") is not True:
        failures.append("STRUCTURAL_VALIDATION_POST_P13.pass")
    if reader.get("result") != "PASS":
        failures.append("READER_STRUCTURAL_QA_POST_P13.result")
    if mechanical.get("result") != "PASS":
        failures.append("READER_MECHANICAL_RENDER_QA_POST_P13.result")
    scope = str(mechanical.get("assessment_scope", "")).casefold()
    if "no visual inspection" not in scope:
        failures.append("READER_MECHANICAL_RENDER_QA_POST_P13.scope_disclaimer")
    if (
        visual.get("inspection_status") != "COMPLETE"
        or visual.get("overall_result") != "PASS"
        or visual.get("inspection_kind")
        != "actual-rendered-page-model-visual-inspection"
    ):
        failures.append("READER_VISUAL_INSPECTION_POST_P13.completion")
    page_count = visual.get("page_count")
    coverage = visual.get("coverage")
    reviewed_pages = coverage.get("reviewed_pages") if isinstance(coverage, dict) else None
    if (
        not isinstance(page_count, int)
        or page_count < 1
        or reviewed_pages != list(range(1, page_count + 1))
    ):
        failures.append("READER_VISUAL_INSPECTION_POST_P13.full_page_coverage")
    criteria = visual.get("criteria")
    if not isinstance(criteria, list) or any(
        not isinstance(item, dict) or item.get("status") not in {"PASS", "NOT_APPLICABLE"}
        for item in criteria
    ):
        failures.append("READER_VISUAL_INSPECTION_POST_P13.criteria")
    reader_state = qa_state.get("reader")
    if not isinstance(reader_state, dict) or any(
        reader_state.get(key) != "PASS"
        for key in (
            "source_structure_qa",
            "pdf_structural_qa",
            "mechanical_render_qa",
            "actual_visual_inspection",
        )
    ):
        failures.append("QA_STATE.reader")
    else:
        expected_reader_hash = reader_state.get("sha256")
        expected_reader_pages = reader_state.get("pages")
        if (
            reader.get("sha256") != expected_reader_hash
            or visual.get("pdf_sha256") != expected_reader_hash
            or reader.get("page_count") != expected_reader_pages
            or page_count != expected_reader_pages
        ):
            failures.append("QA receipt reader identity agreement")
    semantic_state = qa_state.get("semantic_and_formula_audit")
    if not isinstance(semantic_state, dict) or semantic_state.get("result") != (
        "PASS_POST_P13_AFTER_REPAIRS"
    ):
        failures.append("QA_STATE.semantic_and_formula_audit")
    if failures:
        raise RuntimeError("Required post-P13 QA gates failed: " + ", ".join(failures))
    return {
        "post_p13_structure": "PASS",
        "reader_structure": "PASS",
        "mechanical_render": "PASS_WITH_NO_VISUAL_CLAIM",
        "actual_visual_inspection": "PASS",
        "visually_inspected_pages": page_count,
        "semantic_and_formula_audit": "PASS_POST_P13_AFTER_REPAIRS",
        "result": "PASS",
    }


def write_zip(target: Path, root: Path, entries: list[PreparedEntry]) -> None:
    ensure_within(target, root)
    if target.exists():
        raise FileExistsError(f"Refusing to overwrite archive: {target}")
    names = [entry.arcname for entry in sorted(entries, key=lambda item: item.arcname)]
    validate_member_set(names, enforce_order=True)
    assert_entries_unchanged(entries)
    with zipfile.ZipFile(
        target,
        "x",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=ZIP_COMPRESSION_LEVEL,
        allowZip64=True,
        strict_timestamps=True,
    ) as archive:
        archive.comment = b""
        for entry in sorted(entries, key=lambda item: item.arcname):
            info = zipfile.ZipInfo(entry.arcname, FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.internal_attr = 0
            info.extra = b""
            info.comment = b""
            info.file_size = entry.size
            info._compresslevel = ZIP_COMPRESSION_LEVEL
            with archive.open(info, "w", force_zip64=False) as member:
                if entry.data is not None:
                    member.write(entry.data)
                else:
                    assert entry.source is not None
                    with entry.source.open("rb") as source:
                        shutil.copyfileobj(source, member, length=STREAM_BLOCK_SIZE)


def inspect_zip(
    path: Path,
    *,
    expected: dict[str, tuple[int, str]] | None,
    expected_time: tuple[int, int, int, int, int, int],
    allowed_compressions: set[int],
    enforce_order: bool,
    scan_content: bool,
    scan_absolute_paths: bool,
) -> dict[str, object]:
    records: list[tuple[str, int, str]] = []
    content_hits: list[dict[str, object]] = []
    with zipfile.ZipFile(path) as archive:
        if archive.comment:
            raise RuntimeError(f"ZIP archive comment is prohibited: {path.name}")
        names = archive.namelist()
        validate_member_set(names, enforce_order=enforce_order)
        for name in names:
            reject_internal_public_name(name)
        if expected is not None and set(names) != set(expected):
            missing = sorted(set(expected) - set(names))
            extra = sorted(set(names) - set(expected))
            raise RuntimeError(
                f"Unexpected ZIP member set in {path.name}; missing={missing}; extra={extra}"
            )
        crc_failure = archive.testzip()
        if crc_failure is not None:
            raise RuntimeError(f"ZIP CRC failure in {path.name}: {crc_failure}")
        for info in archive.infolist():
            if info.is_dir():
                raise RuntimeError(f"Directory ZIP members are prohibited: {info.filename}")
            if info.flag_bits & 0x1:
                raise RuntimeError(f"Encrypted ZIP member is prohibited: {info.filename}")
            if info.flag_bits & ~0x800:
                raise RuntimeError(
                    f"Unsupported ZIP member flags for {info.filename}: {info.flag_bits:#x}"
                )
            if info.create_system != 3:
                raise RuntimeError(f"Non-Unix ZIP metadata for {info.filename}")
            mode = info.external_attr >> 16
            if not stat.S_ISREG(mode) or stat.S_IMODE(mode) != 0o644:
                raise RuntimeError(f"Unsafe ZIP member mode for {info.filename}: {mode:#o}")
            if info.date_time != expected_time:
                raise RuntimeError(
                    f"Unexpected ZIP timestamp for {info.filename}: {info.date_time}"
                )
            if info.compress_type not in allowed_compressions:
                raise RuntimeError(
                    f"Unsupported ZIP compression for {info.filename}: {info.compress_type}"
                )
            if info.extra or info.comment:
                raise RuntimeError(f"ZIP member extra/comment data is prohibited: {info.filename}")
            digest = hashlib.sha256()
            size = 0
            with archive.open(info) as member:
                carry = b""
                labels: set[str] = set()
                patterns = patterns_for_payload(
                    info.filename,
                    include_absolute_paths=scan_absolute_paths,
                )
                for block in iter(lambda: member.read(STREAM_BLOCK_SIZE), b""):
                    digest.update(block)
                    size += len(block)
                    if scan_content and content_is_scannable(info.filename):
                        scan_block = carry + block
                        for label, pattern in patterns:
                            if label not in labels and pattern.search(scan_block):
                                labels.add(label)
                        carry = scan_block[-SCAN_OVERLAP:]
            actual_digest = digest.hexdigest().upper()
            if size != info.file_size:
                raise RuntimeError(f"ZIP size accounting mismatch for {info.filename}")
            if labels:
                content_hits.append(
                    {"name": info.filename, "finding_labels": sorted(labels)}
                )
            if expected is not None:
                wanted_size, wanted_digest = expected[info.filename]
                if (size, actual_digest) != (wanted_size, wanted_digest):
                    raise RuntimeError(f"ZIP member hash mismatch: {info.filename}")
            records.append((info.filename, size, actual_digest))
    if content_hits:
        raise RuntimeError(
            f"Public-safety scan failed inside {path.name}: "
            + json.dumps(content_hits, ensure_ascii=False)
        )
    fingerprint = hashlib.sha256()
    for name, size, digest in sorted(records):
        fingerprint.update(f"{name}\t{size}\t{digest}\n".encode("utf-8"))
    return {
        "entries": len(records),
        "payload_bytes": sum(record[1] for record in records),
        "member_set_sha256": fingerprint.hexdigest().upper(),
        "crc_failure": None,
        "duplicate_names": 0,
        "casefold_collisions": 0,
        "encrypted_members": 0,
        "unsafe_member_names": 0,
        "content_scan_findings": 0,
        "pass": True,
    }


def expected_map(entries: Iterable[PreparedEntry]) -> dict[str, tuple[int, str]]:
    return {entry.arcname: (entry.size, entry.digest) for entry in entries}


def verify_french_package(
    french_root: Path, french_artifact_directory: Path
) -> tuple[list[PreparedEntry], dict[str, object]]:
    artifact_names = {
        name for name, location, _, _ in FRENCH_PUBLIC_PINS if location == "artifact"
    }
    actual_artifact_names = {
        path.name for path in french_artifact_directory.iterdir() if path.is_file()
    }
    if actual_artifact_names != artifact_names:
        raise RuntimeError(
            "French published artifact directory is not the frozen four-file set; "
            f"missing={sorted(artifact_names - actual_artifact_names)}; "
            f"extra={sorted(actual_artifact_names - artifact_names)}"
        )

    entries: list[PreparedEntry] = []
    records: list[dict[str, object]] = []
    for name, location, wanted_size, wanted_hash in FRENCH_PUBLIC_PINS:
        directory = french_artifact_directory if location == "artifact" else french_root
        source = require_regular_file(directory / name, (directory,))
        actual_size = source.stat().st_size
        actual_hash = sha256(source)
        if (actual_size, actual_hash) != (wanted_size, wanted_hash):
            raise RuntimeError(
                f"Frozen French public member mismatch: {name}; "
                f"expected {wanted_size}/{wanted_hash}, got {actual_size}/{actual_hash}"
            )
        entry = PreparedEntry(
            f"{FRENCH_ARCHIVE_PREFIX}/{name}",
            actual_size,
            actual_hash,
            source=source,
        )
        entries.append(entry)
        records.append(
            {
                "name": name,
                "kind": location,
                "bytes": actual_size,
                "sha256": actual_hash,
                "frozen_pin_match": True,
            }
        )

    manifest_path = french_artifact_directory / "03_GALOIS_1897_FR_SHA256_MANIFEST.txt"
    manifest_lines = manifest_path.read_text(encoding="utf-8").splitlines()
    artifact_rows = [row for row in FRENCH_PUBLIC_PINS if row[1] == "artifact"][:3]
    wanted_lines = [
        f"# Exact release DOI: {FRENCH_EXACT_DOI}",
        f"# Stable concept DOI: {FRENCH_CONCEPT_DOI}",
        "filename\tbytes\tsha256",
        *(f"{name}\t{size}\t{digest}" for name, _, size, digest in artifact_rows),
    ]
    if manifest_lines != wanted_lines:
        raise RuntimeError("Frozen French SHA-256 manifest content is not exact")

    nested_checks = {
        "01_GALOIS_1897_FR_EDITABLE_SOURCES.zip": inspect_zip(
            french_artifact_directory / "01_GALOIS_1897_FR_EDITABLE_SOURCES.zip",
            expected=None,
            expected_time=FRENCH_FIXED_TIME,
            allowed_compressions={zipfile.ZIP_DEFLATED},
            enforce_order=True,
            scan_content=True,
            # The frozen published source contains a documented system-font path.
            # It is immutable and hash-pinned; personal paths remain prohibited in
            # every newly generated English payload.
            scan_absolute_paths=False,
        ),
        "02_GALOIS_1897_FR_EVIDENCE_AND_PROVENANCE.zip": inspect_zip(
            french_artifact_directory / "02_GALOIS_1897_FR_EVIDENCE_AND_PROVENANCE.zip",
            expected=None,
            expected_time=FRENCH_FIXED_TIME,
            allowed_compressions={zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED},
            enforce_order=False,
            scan_content=True,
            scan_absolute_paths=False,
        ),
    }
    # The four non-ZIP frozen members must also be free of local paths/secrets.
    non_zip_entries = [entry for entry in entries if not entry.arcname.endswith(".zip")]
    assert_public_entries_safe(non_zip_entries, "french-public-sibling")
    return entries, {
        "exact_doi": FRENCH_EXACT_DOI,
        "concept_doi": FRENCH_CONCEPT_DOI,
        "frozen_members": records,
        "nested_archive_checks": nested_checks,
        "all_eight_frozen_pins_match": True,
        "result": "PASS",
    }


def _looks_like_whole_local_path(value: str) -> bool:
    if re.match(r"(?i)^[A-Z]:[\\/]", value):
        return True
    if value.startswith("\\\\"):
        return True
    return bool(re.match(r"(?i)^/(?:home|Users|tmp|var/tmp)/", value))


def _path_basename(value: str) -> str:
    if re.match(r"(?i)^[A-Z]:[\\/]", value) or value.startswith("\\\\"):
        return PureWindowsPath(value).name or "location"
    return PurePosixPath(value).name or "location"


def redact_local_paths(value: str) -> str:
    if _looks_like_whole_local_path(value):
        return f"local-private-custody/{_path_basename(value)}"
    value = _FILE_URI_TEXT.sub("[local-file-uri-omitted]", value)
    value = _WINDOWS_PATH_TEXT.sub("[local-path-omitted]", value)
    return _UNIX_PATH_TEXT.sub("[local-path-omitted]", value)


def sanitize_json_value(value: object) -> object:
    if isinstance(value, dict):
        return {str(key): sanitize_json_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [sanitize_json_value(item) for item in value]
    if isinstance(value, str):
        return redact_local_paths(value)
    return value


def make_public_projection(source: Path, kind: str) -> bytes:
    source_data = source.read_bytes()
    source_record = {
        "source_name": source.name,
        "source_bytes": len(source_data),
        "source_sha256": sha256_bytes(source_data),
        "projection_policy": (
            "Substantive content preserved; local absolute paths replaced; "
            "private source retained unchanged in local custody."
        ),
    }
    if kind == "text":
        text = source_data.decode("utf-8")
        header = (
            "<!-- PUBLIC PROJECTION\n"
            f"source_name: {source_record['source_name']}\n"
            f"source_bytes: {source_record['source_bytes']}\n"
            f"source_sha256: {source_record['source_sha256']}\n"
            "policy: substantive content preserved; local absolute paths replaced; "
            "private source retained unchanged in local custody.\n"
            "-->\n\n"
        )
        return (header + redact_local_paths(text).rstrip() + "\n").encode("utf-8")

    parsed = json.loads(source_data.decode("utf-8"))
    if not isinstance(parsed, dict):
        raise ValueError(f"Public JSON projection source must be an object: {source}")
    if kind == "web_receipt":
        if "authority_folder" not in parsed:
            raise ValueError("Web-return receipt lacks the expected custody-path field")
        parsed.pop("authority_folder")
        parsed["authority_folder_public"] = (
            "private local custody; absolute authority path intentionally omitted"
        )
        parsed["receipt_schema"] = (
            "galois.post_p13.individual_download_validation.public.v1"
        )
    elif kind == "visual_receipt":
        reviewer = parsed.get("reviewer")
        if not isinstance(reviewer, dict) or "session_or_task_id" not in reviewer:
            raise ValueError("Visual receipt lacks the expected private task identifier")
        reviewer["session_or_task_id"] = "private-task-id-omitted"
        source_record["projection_policy"] = (
            "Substantive content preserved; local absolute paths and private task "
            "identifier replaced; private schema-valid source retained unchanged."
        )
    projected = sanitize_json_value(parsed)
    assert isinstance(projected, dict)
    if "_public_projection" in projected:
        raise ValueError(f"Projection metadata key already exists: {source}")
    projected["_public_projection"] = source_record
    data = json_bytes(projected)
    hits = scan_bytes(data)
    if hits:
        raise RuntimeError(
            f"Sanitized projection still fails public-safety scan for {source.name}: "
            + ", ".join(hits)
        )
    return data


def build_source_entries(
    root: Path,
    english: Path,
    frozen_english_entries: Iterable[PreparedEntry],
) -> list[PreparedEntry]:
    frozen_by_name = {entry.arcname: entry for entry in frozen_english_entries}
    entries = []
    for relative in SOURCE_FILE_ALLOWLIST:
        frozen = frozen_by_name[relative]
        entries.append(
            PreparedEntry(
                f"source/english/{relative}",
                frozen.size,
                frozen.digest,
                source=frozen.source,
            )
        )
    entries.extend(
        prepare_file_entry(root / name, name, (root,))
        for name in ROOT_METADATA_ALLOWLIST
    )
    entries.extend(
        prepare_file_entry(root / relative, relative, (root,))
        for relative in SOURCE_SIDECAR_ALLOWLIST
    )
    entries.extend(
        prepare_file_entry(
            WORKSPACE / name,
            f"build/{name}",
            (WORKSPACE,),
        )
        for name in BUILD_SCRIPT_ALLOWLIST
    )
    validate_member_set([entry.arcname for entry in entries], enforce_order=False)
    return entries


def build_evidence_entries(root: Path, stage: Path) -> tuple[list[PreparedEntry], list[dict[str, object]]]:
    entries = [
        prepare_file_entry(root / relative, relative, (root,))
        for relative in (
            *EVIDENCE_EXACT_ALLOWLIST,
            *CRITICAL_BASELINE_ALLOWLIST,
            *WEB_RETURN_SUBSTANTIVE_ALLOWLIST,
        )
    ]
    projection_records: list[dict[str, object]] = []
    for relative, arcname, kind in PUBLIC_PROJECTION_SPECS:
        source = require_regular_file(root / relative, (root,))
        source_size = source.stat().st_size
        source_hash = sha256(source)
        data = make_public_projection(source, kind)
        if (source.stat().st_size, sha256(source)) != (source_size, source_hash):
            raise RuntimeError(f"Projection source changed during read: {relative}")
        staged_name = arcname.replace("/", "__")
        if not _SAFE_LEAF.fullmatch(staged_name):
            raise ValueError(f"Unsafe staged projection filename: {staged_name}")
        staged_path = stage / staged_name
        write_new_bytes(staged_path, data, stage)
        entry = prepare_file_entry(staged_path, arcname, (stage,))
        entries.append(entry)
        projection_records.append(
            {
                "private_source_name": PurePosixPath(relative).name,
                "private_source_bytes": source_size,
                "private_source_sha256": source_hash,
                "public_member": arcname,
                "public_bytes": entry.size,
                "public_sha256": entry.digest,
                "local_paths_removed": True,
            }
        )
    validate_member_set([entry.arcname for entry in entries], enforce_order=False)
    return entries, projection_records


def public_file_record(path: Path) -> dict[str, object]:
    return {"name": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}


def make_prepackage_receipt(
    reader: Path,
    source_zip: Path,
    other_zip: Path,
    source_entries: list[PreparedEntry],
    evidence_entries: list[PreparedEntry],
    projection_records: list[dict[str, object]],
    french_verification: dict[str, object],
    source_zip_check: dict[str, object],
    other_zip_check: dict[str, object],
    public_scan_count: int,
    opaque_payload_count: int,
    qa_gates: dict[str, object],
) -> bytes:
    planned_names = sorted(
        [entry.arcname for entry in evidence_entries] + [PREPACKAGE_RECEIPT_ARCNAME]
    )
    receipt = {
        "schema_version": 1,
        "receipt_role": "deterministic pre-package public evidence validation",
        "receipt_created_before_evidence_zip": True,
        "evidence_archive_accounting": {
            "archive_name": EVIDENCE_ZIP_NAME,
            "planned_member_names": planned_names,
            "planned_member_count": len(planned_names),
            "members_excluding_this_receipt": [
                entry.public_record()
                for entry in sorted(evidence_entries, key=lambda item: item.arcname)
            ],
            "receipt_member_hash_omitted_to_avoid_self_reference": True,
            "archive_hash_and_crc_recorded_after_creation_in_external_release_receipt": True,
        },
        "reader": public_file_record(reader),
        "source_archive": public_file_record(source_zip),
        "other_translations_archive": public_file_record(other_zip),
        "qa_gates": qa_gates,
        "source_input_fingerprint_sha256": entry_fingerprint(source_entries),
        "evidence_input_fingerprint_sha256": entry_fingerprint(evidence_entries),
        "public_projection_records": projection_records,
        "french_public_sibling": french_verification,
        "completed_archive_checks": {
            SOURCE_ZIP_NAME: source_zip_check,
            OTHER_TRANSLATIONS_NAME: other_zip_check,
        },
        "public_safety": {
            "pattern_scanned_payloads_before_packaging": public_scan_count,
            "opaque_or_frozen_binary_payloads_hash_validated": opaque_payload_count,
            "scan_scope": (
                "All text/JSON/source payloads; printable path and secret signatures "
                "in PDFs/images; ZIP members inspected after decompression. Frozen "
                "French nested archives are hash-pinned and secret-scanned, with "
                "their pre-published absolute-path content treated as immutable."
            ),
            "secret_findings": 0,
            "new_english_payload_absolute_path_findings": 0,
            "frozen_french_nested_absolute_path_scan": "NOT_CLAIMED",
            "internal_workflow_members": 0,
            "result": "PASS",
        },
        "result": "PASS",
    }
    return json_bytes(receipt)


def manifest_bytes(paths: Iterable[Path]) -> bytes:
    lines = [
        f"Exact DOI: {ENGLISH_EXACT_DOI}",
        f"Concept DOI: {ENGLISH_CONCEPT_DOI}",
        "SHA256  BYTES  FILENAME",
    ]
    lines.extend(
        f"{sha256(path)}  {path.stat().st_size}  {path.name}" for path in paths
    )
    return ("\n".join(lines) + "\n").encode("utf-8")


def validate_manifest(path: Path, payloads: list[Path]) -> dict[str, object]:
    expected = manifest_bytes(payloads)
    actual = path.read_bytes()
    if actual != expected:
        raise RuntimeError("English SHA-256 manifest is not the exact canonical form")
    lines = actual.decode("utf-8").splitlines()
    if len(lines) != 3 + len(payloads):
        raise RuntimeError("English SHA-256 manifest has an unexpected record count")
    names = [line.rsplit("  ", 1)[-1] for line in lines[3:]]
    wanted_names = [READER_NAME, SOURCE_ZIP_NAME, EVIDENCE_ZIP_NAME, OTHER_TRANSLATIONS_NAME]
    if names != wanted_names:
        raise RuntimeError(f"English SHA-256 manifest member order mismatch: {names}")
    return {
        "exact_doi": ENGLISH_EXACT_DOI,
        "concept_doi": ENGLISH_CONCEPT_DOI,
        "payload_records": len(payloads),
        "self_hashing": False,
        "canonical_bytes_match": True,
        "result": "PASS",
    }


def compare_public_outputs(
    reference: Path, current: dict[str, Path]
) -> dict[str, object]:
    comparisons: list[dict[str, object]] = []
    mismatches: list[str] = []
    for name in PUBLIC_FILE_NAMES:
        reference_file = require_regular_file(reference / name, (reference,))
        current_file = current[name]
        reference_record = public_file_record(reference_file)
        current_record = public_file_record(current_file)
        identical = (
            reference_record["bytes"],
            reference_record["sha256"],
        ) == (current_record["bytes"], current_record["sha256"])
        comparisons.append(
            {
                "name": name,
                "bytes": current_record["bytes"],
                "sha256": current_record["sha256"],
                "byte_identical": identical,
            }
        )
        if not identical:
            mismatches.append(name)
    if mismatches:
        raise RuntimeError(
            "Two-build byte-identity failure for: " + ", ".join(mismatches)
        )
    return {
        "status": "PASS",
        "reference_output_directory": reference.name,
        "compared_files": len(comparisons),
        "files": comparisons,
        "all_five_byte_identical": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build into new directories only; retain every build/output directory. "
            "Use --establish-comparison-baseline on the first retained run, then "
            "--compare-to-output-directory on the required release run."
        )
    )
    parser.add_argument("root", nargs="?", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--french-root", type=Path, default=DEFAULT_FRENCH_ROOT)
    parser.add_argument(
        "--french-artifact-directory",
        type=Path,
        default=DEFAULT_FRENCH_ARTIFACT_DIRECTORY,
    )
    parser.add_argument("--output-directory", required=True)
    parser.add_argument("--build-directory", required=True)
    comparison_mode = parser.add_mutually_exclusive_group(required=True)
    comparison_mode.add_argument("--establish-comparison-baseline", action="store_true")
    comparison_mode.add_argument("--compare-to-output-directory")
    args = parser.parse_args()

    output_name = validate_leaf_name(args.output_directory, "--output-directory")
    build_name = validate_leaf_name(args.build_directory, "--build-directory")
    reference_name = None
    if args.compare_to_output_directory is not None:
        reference_name = validate_leaf_name(
            args.compare_to_output_directory, "--compare-to-output-directory"
        )
        if reference_name.casefold() == output_name.casefold():
            raise ValueError(
                "Comparison and current output directories must differ, including case"
            )

    root = args.root.resolve(strict=True)
    french_root = args.french_root.resolve(strict=True)
    french_artifact_directory = args.french_artifact_directory.resolve(strict=True)
    if not root.is_dir() or not french_root.is_dir() or not french_artifact_directory.is_dir():
        raise NotADirectoryError("All declared publication roots must be directories")
    english = root / "source" / "english"
    if not english.is_dir():
        raise NotADirectoryError(f"English source directory is missing: {english}")

    output = root / output_name
    final_build = root / "build" / build_name
    reference_resolved: Path | None = None
    if reference_name is not None:
        reference_output = root / reference_name
        ensure_within(reference_output, root)
        if not reference_output.is_dir():
            raise FileNotFoundError(
                f"Comparison output directory must preexist this build: {reference_output}"
            )
        # Resolve before claiming current directories, and reject aliases/junctions.
        reference_resolved = reference_output.resolve(strict=True)
        output_prospective = output.resolve(strict=False)
        if (
            reference_resolved == output_prospective
            or str(reference_resolved).casefold() == str(output_prospective).casefold()
        ):
            raise ValueError("Comparison output aliases the current output directory")
        for name in PUBLIC_FILE_NAMES:
            require_regular_file(reference_resolved / name, (reference_resolved,))
    if output.exists() or final_build.exists():
        existing = [str(path) for path in (output, final_build) if path.exists()]
        raise FileExistsError(
            "Refusing to reuse existing build/output paths: " + "; ".join(existing)
        )

    audit_source_inventory(english)
    build_input_entries = [
        prepare_file_entry(english / relative, relative, (english,))
        for relative in SOURCE_FILE_ALLOWLIST
    ]
    # Validate every allowlisted non-build input before claiming output directories.
    for relative in (
        *ROOT_METADATA_ALLOWLIST,
        *SOURCE_SIDECAR_ALLOWLIST,
        *EVIDENCE_EXACT_ALLOWLIST,
        *CRITICAL_BASELINE_ALLOWLIST,
        *WEB_RETURN_SUBSTANTIVE_ALLOWLIST,
        *(spec[0] for spec in PUBLIC_PROJECTION_SPECS),
    ):
        require_regular_file(root / relative, (root,))
    for name in BUILD_SCRIPT_ALLOWLIST:
        require_regular_file(WORKSPACE / name, (WORKSPACE,))

    qa_gates = validate_qa_receipts(root)

    french_entries, french_verification = verify_french_package(
        french_root, french_artifact_directory
    )

    # Atomic mkdir is the only claiming operation. Existing—even empty—directories
    # are never reused, and this builder has no cleanup/delete code path.
    claim_new_directory(final_build, root)
    claim_new_directory(output, root)

    command = [
        "latexmk",
        "-pdf",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        f"-outdir={final_build}",
        "GAL1897_EN_MODERN_READER.tex",
    ]
    result = subprocess.run(command, cwd=english, check=False)
    if result.returncode:
        return result.returncode
    assert_entries_unchanged(build_input_entries)

    built = require_regular_file(
        final_build / "GAL1897_EN_MODERN_READER.pdf", (final_build,)
    )
    qa_reader_state = json.loads(
        (root / "evidence" / "QA_STATE.json").read_text(encoding="utf-8")
    )["reader"]
    if (built.stat().st_size, sha256(built)) != (
        qa_reader_state["bytes"],
        qa_reader_state["sha256"],
    ):
        raise RuntimeError(
            "Freshly built reader does not match the exact reader audited by the "
            "post-P13 structural, render, and visual receipts"
        )
    reader = output / READER_NAME
    with built.open("rb") as source, reader.open("xb") as target:
        shutil.copyfileobj(source, target, length=STREAM_BLOCK_SIZE)
    reader_hits: tuple[str, ...]
    with reader.open("rb") as stream:
        reader_hits = scan_named_stream(stream, READER_NAME)
    if reader_hits:
        raise RuntimeError(
            "Built reader failed public-safety scan: " + ", ".join(reader_hits)
        )

    source_zip = output / SOURCE_ZIP_NAME
    source_entries = build_source_entries(root, english, build_input_entries)
    source_scan_count = assert_public_entries_safe(source_entries, "source-archive")
    write_zip(source_zip, root, source_entries)
    source_zip_check = inspect_zip(
        source_zip,
        expected=expected_map(source_entries),
        expected_time=FIXED_TIME,
        allowed_compressions={zipfile.ZIP_DEFLATED},
        enforce_order=True,
        scan_content=True,
        scan_absolute_paths=True,
    )
    assert_entries_unchanged(source_entries)
    assert_entries_unchanged(build_input_entries)

    other_zip = output / OTHER_TRANSLATIONS_NAME
    assert_entries_unchanged(french_entries)
    write_zip(other_zip, root, french_entries)
    other_zip_check = inspect_zip(
        other_zip,
        expected=expected_map(french_entries),
        expected_time=FIXED_TIME,
        allowed_compressions={zipfile.ZIP_DEFLATED},
        enforce_order=True,
        # Nested frozen ZIPs were separately validated; treat their compressed bytes
        # as opaque here while scanning all non-ZIP members before this archive write.
        scan_content=False,
        scan_absolute_paths=False,
    )
    assert_entries_unchanged(french_entries)

    stage = final_build / "public-package-inputs"
    stage.mkdir()
    evidence_entries, projection_records = build_evidence_entries(root, stage)
    evidence_scan_count = assert_public_entries_safe(
        evidence_entries, "evidence-archive"
    )
    prepackage_data = make_prepackage_receipt(
        reader,
        source_zip,
        other_zip,
        source_entries,
        evidence_entries,
        projection_records,
        french_verification,
        source_zip_check,
        other_zip_check,
        sum(
            content_is_scannable(entry.arcname)
            for entry in (*source_entries, *evidence_entries)
        ),
        1
        + sum(
            not content_is_scannable(entry.arcname)
            for entry in (*source_entries, *evidence_entries)
        )
        + len(french_entries),
        qa_gates,
    )
    if scan_bytes(prepackage_data):
        raise RuntimeError("Generated pre-package receipt is not public-safe")
    prepackage_path = stage / "PREPACKAGE_VALIDATION_RECEIPT.json"
    write_new_bytes(prepackage_path, prepackage_data, stage)
    evidence_entries.append(
        prepare_file_entry(
            prepackage_path,
            PREPACKAGE_RECEIPT_ARCNAME,
            (stage,),
        )
    )

    evidence_zip = output / EVIDENCE_ZIP_NAME
    write_zip(evidence_zip, root, evidence_entries)
    evidence_zip_check = inspect_zip(
        evidence_zip,
        expected=expected_map(evidence_entries),
        expected_time=FIXED_TIME,
        allowed_compressions={zipfile.ZIP_DEFLATED},
        enforce_order=True,
        scan_content=True,
        scan_absolute_paths=True,
    )

    manifest_payloads = [reader, source_zip, evidence_zip, other_zip]
    manifest = output / MANIFEST_NAME
    write_new_bytes(manifest, manifest_bytes(manifest_payloads), root)
    manifest_check = validate_manifest(manifest, manifest_payloads)
    with manifest.open("rb") as stream:
        manifest_hits = scan_stream(stream)
    if manifest_hits:
        raise RuntimeError(
            "Manifest failed public-safety scan: " + ", ".join(manifest_hits)
        )

    public_paths = {
        READER_NAME: reader,
        SOURCE_ZIP_NAME: source_zip,
        EVIDENCE_ZIP_NAME: evidence_zip,
        MANIFEST_NAME: manifest,
        OTHER_TRANSLATIONS_NAME: other_zip,
    }
    comparison = (
        compare_public_outputs(reference_resolved, public_paths)
        if reference_resolved is not None
        else {
            "status": "BASELINE_ESTABLISHED_SECOND_BUILD_REQUIRED",
            "compared_files": 0,
            "all_five_byte_identical": False,
        }
    )

    archive_checks = {
        SOURCE_ZIP_NAME: source_zip_check,
        EVIDENCE_ZIP_NAME: evidence_zip_check,
        OTHER_TRANSLATIONS_NAME: other_zip_check,
    }
    receipt = {
        "schema_version": 2,
        "result": (
            "PASS"
            if comparison["all_five_byte_identical"]
            else "BASELINE_ESTABLISHED_SECOND_BUILD_REQUIRED"
        ),
        "output_directory": output_name,
        "build_directory": f"build/{build_name}",
        "non_destructive_policy": {
            "new_output_directory_claimed": True,
            "new_build_directory_claimed": True,
            "existing_directories_reused": False,
            "recursive_cleanup_performed": False,
        },
        "reader": public_file_record(reader),
        "public_files": [
            public_file_record(public_paths[name]) for name in PUBLIC_FILE_NAMES
        ],
        "source_allowlist": {
            "archive_entries": len(source_entries),
            "input_fingerprint_sha256": entry_fingerprint(source_entries),
            "source_authority_sidecar_included": True,
            "datacite_relations_sidecar_included": True,
        },
        "evidence_allowlist": {
            "archive_entries": len(evidence_entries),
            "input_fingerprint_sha256": entry_fingerprint(evidence_entries),
            "prepackage_receipt_preexisted_archive": True,
            "public_projection_records": projection_records,
            "internal_durable_state_included": False,
            "incident_or_return_logs_included": False,
        },
        "french_public_sibling": french_verification,
        "archive_checks": archive_checks,
        "qa_gates": qa_gates,
        "manifest_check": manifest_check,
        "public_safety": {
            "scan_scope": (
                "All text/JSON/source payloads; best-effort printable path and secret "
                "signatures in raw PDF/image bytes; every generated ZIP member "
                "hash/CRC/name/mode validated after decompression. This is not a "
                "format-aware PDF/image metadata or rendered-content scan."
            ),
            "new_english_pattern_scan_secret_findings": 0,
            "new_english_pattern_scan_absolute_path_findings": 0,
            "frozen_french_nested_absolute_path_scan": "NOT_CLAIMED",
            "unsafe_zip_names": 0,
            "credential_or_internal_workflow_members": 0,
            "result": "PASS",
        },
        "two_build_byte_identity": comparison,
    }
    receipt_data = json_bytes(receipt)
    receipt_hits = scan_bytes(receipt_data)
    if receipt_hits:
        raise RuntimeError(
            "Final release receipt failed public-safety scan: "
            + ", ".join(receipt_hits)
        )
    write_new_bytes(output / RELEASE_RECEIPT_NAME, receipt_data, root)
    exact_output_names = set(PUBLIC_FILE_NAMES) | {RELEASE_RECEIPT_NAME}
    actual_output_names = {path.name for path in output.iterdir()}
    if actual_output_names != exact_output_names or any(
        not path.is_file() or path.is_symlink() for path in output.iterdir()
    ):
        raise RuntimeError(
            "Final output directory is not the exact five-file public package plus "
            "external build receipt"
        )
    print(receipt_data.decode("utf-8"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
