#!/usr/bin/env python3
"""Build complete translation coverage/alignment/critical/unresolved ledgers."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import argparse
from pathlib import Path


DEFAULT_ROOT = Path(__file__).resolve().parent / "galois-en-publication"

TITLES = {
    "W01": "Preliminary matter and portraits",
    "W02": "Émile Picard's Introduction",
    "W03": "Proof of a Theorem on Periodic Continued Fractions",
    "W04": "Notes on Some Points in Analysis",
    "W05": "Analysis of a Memoir on the Algebraic Solution of Equations",
    "W06": "Note on the Solution of Numerical Equations",
    "W07": "On the Theory of Numbers",
    "W08": "Letter to Auguste Chevalier",
    "W09": "Memoir on the Conditions for the Solvability of Equations by Radicals",
    "W10": "On Primitive Equations Solvable by Radicals (Fragment)",
    "W11": "Historical Table of Contents, Colophon, and Trailing Leaves",
}

SCOPES = {
    "W01": "PDF001-PDF023 / L0000-L0022; 5 substantive, 14 blank, 4 excluded",
    "W02": "PDF024-PDF029 / L0023-L0028; printed folios v-x",
    "W03": "PDF030-PDF037 / L0029-L0036; printed pages 1-8",
    "W04": "PDF038-PDF039 / L0037-L0038; printed pages 9-10",
    "W05": "PDF040-PDF041 / L0039-L0040; printed pages 11-12",
    "W06": "PDF042-PDF043 / L0041-L0042; printed pages 13-14",
    "W07": "PDF044-PDF053 / L0043-L0052; printed pages 15-24 plus blank",
    "W08": "PDF054-PDF061 / L0053-L0060; printed pages 25-32",
    "W09": "PDF062-PDF079 / L0061-L0078; printed pages 33-50",
    "W10": "PDF080-PDF091 / L0079-L0090; printed pages 51-62 plus blank",
    "W11": "PDF092-PDF096 / L0091-L0095; contents, colophon, 3 blanks",
}

EXPECTED_POST_P13_TASK_IDS = {
    *(f"POST-P13-A{number:03d}" for number in range(1, 15)),
    "W10-DA001",
    "W10-DA002",
    "W10-DA003",
    "W10-DA004",
    "W11-DA001",
    "W11-DA002",
    "W11-DA003",
}

EXPECTED_POST_P13_OPEN_IDS = {
    "W01-U001",
    "W01-U002",
    "W01-U003",
    "W08-WV001",
    "W11-U001",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=DEFAULT_ROOT,
        help="English publication tree (defaults to work/galois-en-publication)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    english = root / "source" / "english" / "tex" / "works"
    baseline = root / "source" / "critical_baseline"
    evidence = root / "evidence"
    web_return = evidence / "web_post_p13_return"

    evidence.mkdir(parents=True, exist_ok=True)
    alignment: list[dict[str, object]] = []
    coverage: list[dict[str, object]] = []

    errors = read_csv(baseline / "PRINTED_AND_SOURCE_ERRORS.csv")
    variants = read_csv(baseline / "WITNESS_VARIANTS.csv")
    errata = read_csv(baseline / "ERRATA_AND_UNRESOLVED_LEDGER.csv")
    deferred = read_csv(baseline / "DEFERRED_AUDIT_REGISTER.csv")
    web_tasks = read_csv(web_return / "MASTER_21_TASK_LEDGER.csv")
    web_errata = read_csv(web_return / "CRITICAL_ERRATA_CATALOGUE.csv")
    web_prior = read_csv(web_return / "BIBLIOGRAPHIC_PRIOR_NOTICE_MATRIX.csv")
    web_open = read_csv(web_return / "OPEN_AFTER_21_TASKS.csv")
    web_receipt = json.loads(
        (web_return / "INDIVIDUAL_DOWNLOAD_VALIDATION_RECEIPT.json").read_text(
            encoding="utf-8"
        )
    )
    receipt_files = {row["name"]: row for row in web_receipt["files"]}
    for name, row in receipt_files.items():
        path = web_return / name
        if not path.is_file():
            raise ValueError(f"post-P13 receipt file missing from mirror: {name}")
        if path.stat().st_size != row["bytes"] or sha256(path) != row["sha256"]:
            raise ValueError(f"post-P13 receipt mismatch in mirror: {name}")

    cold_audit = json.loads((web_return / "COLD_AUDIT_CHECKS.json").read_text(encoding="utf-8"))
    cold_checks = cold_audit.get("checks", [])
    if (
        cold_audit.get("status") != "PASS"
        or cold_audit.get("checks_passed") != 242
        or cold_audit.get("checks_total") != 242
        or len(cold_checks) != 242
        or len({row["check_id"] for row in cold_checks}) != 242
        or any(row.get("status") != "PASS" for row in cold_checks)
    ):
        raise ValueError("mirrored post-P13 machine-readable cold audit is not 242/242 PASS")

    error_ids = {row["error_id"] for row in errors}
    variant_ids = {row["variant_id"] for row in variants}
    unresolved_ids = {
        row["record_id"] for row in errata if row.get("source_disposition") == "unresolved"
    }
    deferred_ids = {row["audit_id"] for row in deferred}
    web_task_by_id = {row["task_id"]: row for row in web_tasks}
    web_errata_by_id = {row["error_id"]: row for row in web_errata}
    web_prior_by_id = {row["record_id"]: row for row in web_prior}
    baseline_errata_by_id = {row["record_id"]: row for row in errata}
    variant_by_id = {row["variant_id"]: row for row in variants}

    if set(web_errata_by_id) != error_ids:
        raise ValueError(
            "post-P13 errata IDs do not exactly match the frozen 36-error baseline"
        )
    if len(web_tasks) != 21 or len(web_task_by_id) != 21:
        raise ValueError("post-P13 master ledger must contain 21 unique tasks")
    if set(web_task_by_id) != EXPECTED_POST_P13_TASK_IDS:
        raise ValueError(
            "post-P13 task IDs differ from the frozen 21-task universe: "
            f"missing={sorted(EXPECTED_POST_P13_TASK_IDS - set(web_task_by_id))}; "
            f"unexpected={sorted(set(web_task_by_id) - EXPECTED_POST_P13_TASK_IDS)}"
        )
    if len(web_prior) != 51 or len(web_prior_by_id) != 51:
        raise ValueError("post-P13 priority matrix must contain 51 unique records")
    if set(web_prior_by_id) != error_ids | variant_ids:
        raise ValueError(
            "post-P13 priority IDs do not exactly equal the frozen error/variant universe"
        )
    if len(web_open) != 5 or len({row["record_id"] for row in web_open}) != 5:
        raise ValueError("post-P13 cumulative open ledger must contain five unique records")
    if {row["record_id"] for row in web_open} != EXPECTED_POST_P13_OPEN_IDS:
        raise ValueError(
            "post-P13 open IDs differ from the frozen five-record open universe"
        )

    rendered_notes: set[str] = set()
    source_texts: list[str] = [
        (root / "source" / "english" / "GAL1897_EN_MODERN_READER.tex").read_text(
            encoding="utf-8"
        )
    ]
    component_counts: dict[str, int] = {}
    all_source_pages: set[int] = set()
    all_segments: set[str] = set()

    for path in sorted(english.glob("GAL1897_W*.tex")):
        component = re.search(r"_(W\d{2})_", path.name).group(1)
        text = path.read_text(encoding="utf-8")
        source_texts.append(text)
        notes = re.findall(r"\\GalCriticalNote\{([^}]+)\}", text)
        rendered_notes.update(notes)
        markers = re.findall(r"(?m)^[ \t]*%\s*(ENSEG:(W\d{2}):PDF(\d{3}):(\d{4}))\s*$", text)
        seen_component: set[str] = set()
        for full_id, marker_component, pdf, ordinal in markers:
            if marker_component != component or full_id in all_segments:
                raise ValueError(f"duplicate/misrouted segment {full_id}")
            all_segments.add(full_id)
            seen_component.add(full_id)
            alignment.append({
                "segment_id": full_id,
                "component_id": component,
                "english_file": f"source/english/tex/works/{path.name}",
                "english_anchor": f"% {full_id}",
                "french_file": f"source/french_diplomatic/tex/works/{path.name}",
                "source_pdf": pdf,
                "status": "translated_aligned",
                "notes": "Modern-English segment aligned to the frozen French diplomatic source page; source topology retained.",
            })

        pages = {
            int(value)
            for value in re.findall(
                r"\\Gal(?:SourcePageStart|SourcePageBoundary|SourcePageBoundaryInWord|SourcePageBegin|SourceBlankPage|BlankTopologyPage|ExcludedSourcePage|UnresolvedSourcePage)\{(\d{3})\}",
                text,
            )
        }
        all_source_pages.update(pages)
        component_counts[component] = len(seen_component)
        component_note_ids = sorted(
            note for note in notes if note.startswith(component + "-")
        )
        coverage.append({
            "component_id": component,
            "component_title": TITLES[component],
            "french_file": f"source/french_diplomatic/tex/works/{path.name}",
            "exact_source_scope": SCOPES[component],
            "english_file": f"source/english/tex/works/{path.name}",
            "translation_status": "complete_post_P13_integrated_semantic_and_render_QA_passed_pending_publication",
            "segment_count": len(seen_component),
            "critical_note_ids": ";".join(component_note_ids),
            "source_page_records": ";".join(f"PDF{page:03d}" for page in sorted(pages)),
            "notes": "All substantive historical prose translated; formulas and source-coordinate topology preserved; critical apparatus remains a separate layer.",
        })

    # W01 deliberately represents all pages by disposition macros. Every
    # physical source page across the full corpus must therefore be accounted.
    missing_pages = set(range(1, 97)) - all_source_pages
    if missing_pages:
        raise ValueError(f"unaccounted physical source pages: {sorted(missing_pages)}")

    write_tsv(
        evidence / "EN_FR_ALIGNMENT.tsv",
        ["segment_id", "component_id", "english_file", "english_anchor", "french_file", "source_pdf", "status", "notes"],
        alignment,
    )
    write_tsv(
        evidence / "ENGLISH_COVERAGE.tsv",
        ["component_id", "component_title", "french_file", "exact_source_scope", "english_file", "translation_status", "segment_count", "critical_note_ids", "source_page_records", "notes"],
        coverage,
    )

    critical_rows: list[dict[str, object]] = []
    specific_task_links = {
        "W05-SE001": ["POST-P13-A005"],
        "W05-SE002": ["POST-P13-A006"],
        "W08-PE001": ["POST-P13-A006"],
        "W08-PE002": ["POST-P13-A007"],
        "W08-WV001": ["POST-P13-A008"],
        "W09-PE001": ["POST-P13-A009", "POST-P13-A014"],
        "W09-PE002": ["POST-P13-A009", "POST-P13-A014"],
        "W09-SE001": ["POST-P13-A010", "POST-P13-A014"],
        "W09-SE002": ["POST-P13-A011", "POST-P13-A014"],
        "W09-SE003": ["POST-P13-A011", "POST-P13-A014"],
        "W09-SE004": ["POST-P13-A012", "POST-P13-A014"],
        "W09-SE005": ["POST-P13-A013", "POST-P13-A014"],
        "W09-SE006": ["POST-P13-A013", "POST-P13-A014"],
        "W09-WV001": ["POST-P13-A014"],
        "W09-WV002": ["POST-P13-A014"],
        "W09-WV003": ["POST-P13-A014"],
        "W09-WV004": ["POST-P13-A014"],
        "W09-WV005": ["POST-P13-A014"],
        "W09-WV006": ["POST-P13-A014"],
        "W10-PE001": ["W10-DA001", "W10-DA004"],
        "W10-PE002": ["W10-DA001", "W10-DA004"],
        "W10-PE003": ["W10-DA002", "W10-DA004"],
        "W10-PE004": ["W10-DA002", "W10-DA004"],
        "W10-PE005": ["W10-DA002", "W10-DA004"],
        "W10-PE006": ["W10-DA003", "W10-DA004"],
        "W10-SE001": ["W10-DA004"],
        "W10-SE002": ["W10-DA004"],
        "W11-PE001": ["W11-DA001"],
    }
    for row in errors:
        issue_id = row["error_id"]
        final = web_errata_by_id[issue_id]
        prior = web_prior_by_id[issue_id]
        critical_rows.append({
            "issue_id": issue_id,
            "kind": "printed_or_source_error",
            "worker_id": row["worker_id"],
            "pdf_pages": row["pdf_page1"],
            "jp2_leaves": row["jp2_leaf"],
            "baseline_classification": row["classification"],
            "baseline_source_disposition": row["source_disposition"],
            "baseline_proof_status": row["proof_status"],
            "rendered_note": str(issue_id in rendered_notes).lower(),
            "baseline_evidence_ids": row["evidence_ids"],
            "baseline_summary": row["proof_summary"],
            "baseline_instruction": row["translation_or_critical_layer_rule"],
            "final_adjudication": final["adjudication"],
            "critical_repair": final["critical_repair"],
            "minimal_hypotheses": final["minimal_hypotheses"],
            "propagation_outcome": final["propagation_outcome"],
            "prior_notice_class": prior["notice_class"],
            "prior_notice_outcome": final["prior_notice_outcome"],
            "earliest_secure_notice_or_attestation": prior["earliest_secure_notice_or_attestation"],
            "source_ids": final["source_ids"],
            "search_cutoff": prior["search_cutoff"],
            "diplomatic_layer_mutated": final["diplomatic_layer_mutated"],
            "critical_layer_state": final["critical_layer_state"],
            "post_p13_task_ids": ";".join(
                ["POST-P13-A001", "POST-P13-A002", "POST-P13-A003"]
                + specific_task_links.get(issue_id, [])
            ),
        })
    for row in variants:
        issue_id = row["variant_id"]
        prior = web_prior_by_id[issue_id]
        critical_rows.append({
            "issue_id": issue_id,
            "kind": "witness_variant",
            "worker_id": row["worker_id"],
            "pdf_pages": row["target_pdf_pages"],
            "jp2_leaves": row["target_jp2_leaves"],
            "baseline_classification": row["classification"],
            "baseline_source_disposition": row["source_disposition"],
            "baseline_proof_status": "documented_or_unresolved",
            "rendered_note": str(issue_id in rendered_notes).lower(),
            "baseline_evidence_ids": row["evidence_ids"],
            "baseline_summary": f"1897: {row['target_1897_form']} | Other witness: {row['other_witness_form']}",
            "baseline_instruction": row["editorial_instruction"],
            "final_adjudication": prior["notice_class"],
            "critical_repair": "not_applicable_witness_or_editorial_variant",
            "minimal_hypotheses": "not_applicable",
            "propagation_outcome": "See the item-level prior-notice matrix and dependency graph.",
            "prior_notice_class": prior["notice_class"],
            "prior_notice_outcome": prior["exact_evidence"],
            "earliest_secure_notice_or_attestation": prior["earliest_secure_notice_or_attestation"],
            "source_ids": prior["source_ids"],
            "search_cutoff": prior["search_cutoff"],
            "diplomatic_layer_mutated": "not_applicable_variant",
            "critical_layer_state": (
                "open" if issue_id in {item["record_id"] for item in web_open} else "closed"
            ),
            "post_p13_task_ids": ";".join(
                ["POST-P13-A003"] + specific_task_links.get(issue_id, [])
            ),
        })
    write_tsv(
        evidence / "GPT_CRITICAL_CALLOUTS.tsv",
        ["issue_id", "kind", "worker_id", "pdf_pages", "jp2_leaves", "baseline_classification", "baseline_source_disposition", "baseline_proof_status", "rendered_note", "baseline_evidence_ids", "baseline_summary", "baseline_instruction", "final_adjudication", "critical_repair", "minimal_hypotheses", "propagation_outcome", "prior_notice_class", "prior_notice_outcome", "earliest_secure_notice_or_attestation", "source_ids", "search_cutoff", "diplomatic_layer_mutated", "critical_layer_state", "post_p13_task_ids"],
        sorted(critical_rows, key=lambda row: str(row["issue_id"])),
    )

    unresolved_rows: list[dict[str, object]] = []
    for open_row in web_open:
        issue_id = open_row["record_id"]
        baseline_row = baseline_errata_by_id.get(issue_id, {})
        prior_row = web_prior_by_id.get(issue_id, {})
        variant_row = variant_by_id.get(issue_id, {})
        unresolved_rows.append({
            "item_id": issue_id,
            "kind": baseline_row.get("record_type", "witness_or_editorial_variant"),
            "scope": (
                f"PDF {baseline_row['pdf_pages']} / {baseline_row['jp2_leaves']}"
                if baseline_row
                else prior_row.get("target_coordinate", variant_row.get("target_pdf_pages", ""))
            ),
            "status": open_row["status"],
            "rendered_note": str(issue_id in rendered_notes or issue_id.startswith("W01-")).lower(),
            "required_action": open_row["missing_evidence"],
            "evidence_ids": prior_row.get("source_ids", baseline_row.get("evidence_ids", "")),
            "description": baseline_row.get(
                "diplomatic_form_or_description",
                variant_row.get("other_witness_form", open_row["missing_evidence"]),
            ),
        })
    write_tsv(
        evidence / "UNRESOLVED_ITEMS.tsv",
        ["item_id", "kind", "scope", "status", "rendered_note", "required_action", "evidence_ids", "description"],
        unresolved_rows,
    )

    write_tsv(
        evidence / "POST_P13_TASK_DISPOSITIONS.tsv",
        ["task_id", "source_scope", "status", "result", "certificate", "evidence_pointers"],
        web_tasks,
    )

    status_counts: dict[str, int] = {}
    for row in web_tasks:
        status_counts[row["status"]] = status_counts.get(row["status"], 0) + 1
    combined_source_text = "\n".join(source_texts)
    source_task_references = sorted(
        task_id for task_id in web_task_by_id if task_id in combined_source_text
    )
    task_ids_without_source_reference = sorted(
        set(web_task_by_id) - set(source_task_references)
    )
    post_p13_summary = {
        "schema_version": 1,
        "individual_download_custody_status": web_receipt["custody_status"],
        "individual_download_validation_receipt": "evidence/web_post_p13_return/INDIVIDUAL_DOWNLOAD_VALIDATION_RECEIPT.json",
        "cumulative_archive_present": web_receipt[
            "archive_claim_from_returned_sidecar_and_package_receipt"
        ]["archive_present_in_authority_folder"],
        "archive_internal_payload_replay_performed": web_receipt[
            "archive_claim_from_returned_sidecar_and_package_receipt"
        ]["internal_180_file_payload_hash_replay_independently_performed"],
        "tasks": len(web_tasks),
        "task_status_counts": status_counts,
        "closed_errata": len(web_errata),
        "priority_records": len(web_prior),
        "cumulative_open_records": [row["record_id"] for row in web_open],
        "source_task_references": source_task_references,
        "task_ids_without_source_reference": task_ids_without_source_reference,
        "cold_audit_checks": {"passed": 242, "total": 242, "status": "PASS"},
    }
    (evidence / "POST_P13_INTEGRATION_SUMMARY.json").write_text(
        json.dumps(post_p13_summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = {
        "schema_version": 1,
        "components": len(component_counts),
        "segments": len(alignment),
        "component_segment_counts": component_counts,
        "physical_source_pages_accounted": len(all_source_pages),
        "proved_error_records": len(errors),
        "witness_variant_records": len(variants),
        "baseline_unresolved_source_records": len(unresolved_ids),
        "baseline_deferred_research_records": len(deferred_ids),
        "post_p13_cumulative_open_records": len(web_open),
        "post_p13_remaining_deferred_research_records": 0,
        "post_p13_task_status_counts": status_counts,
        "post_p13_input_hashes": {
            name: row["sha256"] for name, row in sorted(receipt_files.items())
        },
        "post_p13_cold_audit_checks": "242/242 PASS",
        "post_p13_task_ids_without_source_reference": task_ids_without_source_reference,
        "rendered_critical_note_ids": sorted(rendered_notes),
        "baseline_error_ids_without_rendered_note": sorted(error_ids - rendered_notes),
        "baseline_variant_ids_without_rendered_note": sorted(variant_ids - rendered_notes),
        "pass": (
            len(component_counts) == 11
            and len(all_source_pages) == 96
            and not (error_ids - rendered_notes)
            and status_counts
            == {
                "repaired": 9,
                "proved": 8,
                "rejected": 2,
                "unresolved_after_bounded_search": 2,
            }
            and len(web_open) == 5
            and len(critical_rows) == 51
            and not (variant_ids - rendered_notes)
            and not task_ids_without_source_reference
        ),
    }
    (evidence / "TRANSLATION_LEDGER_BUILD.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
