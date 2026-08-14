#!/usr/bin/env python3
"""Replay the complete merged web-R2 authority and emit a public-safe receipt."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path, PurePosixPath


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def safe_relative(value: str) -> Path:
    posix = PurePosixPath(value)
    if posix.is_absolute() or not posix.parts or any(
        part in {"", ".", ".."} for part in posix.parts
    ):
        raise ValueError(f"unsafe authority path: {value!r}")
    return Path(*posix.parts)


def verify_records(root: Path, rows: list[dict[str, str]], field: str) -> list[str]:
    failures: list[str] = []
    for row in rows:
        relative = safe_relative(row[field])
        path = root / relative
        if not path.is_file():
            failures.append(f"missing:{row[field]}")
            continue
        expected_size = int(row.get("size_bytes") or row.get("bytes") or "-1")
        if path.stat().st_size != expected_size:
            failures.append(f"size:{row[field]}")
            continue
        if sha256(path) != row["sha256"].upper():
            failures.append(f"sha256:{row[field]}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("authority_root", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    root = args.authority_root.resolve(strict=True)
    output = args.output.resolve()
    if not root.is_dir() or output.suffix.lower() != ".json":
        parser.error("authority_root must be a directory and output must be JSON")

    split_manifest_path = root / "SPLIT_SOURCE_CONTENT_MANIFEST.csv"
    split_rows = read_csv(split_manifest_path)
    prefix = root.name + "/"
    normalized_split_rows: list[dict[str, str]] = []
    for row in split_rows:
        archive_path = row["archive_path"]
        if not archive_path.startswith(prefix):
            raise ValueError(f"split archive path lacks expected root prefix: {archive_path}")
        normalized_split_rows.append(
            {**row, "relative_path": archive_path[len(prefix) :]}
        )
    split_failures = verify_records(root, normalized_split_rows, "relative_path")

    package_manifest_path = root / "PACKAGE_MANIFEST.csv"
    package_rows = read_csv(package_manifest_path)
    package_failures = verify_records(root, package_rows, "path")

    errata = read_csv(root / "ledgers" / "CRITICAL_ERRATA_CATALOGUE.csv")
    dependencies = read_csv(root / "ledgers" / "DEPENDENCY_PROPAGATION_EDGES.csv")
    prior = read_csv(root / "ledgers" / "BIBLIOGRAPHIC_PRIOR_NOTICE_MATRIX.csv")
    tasks = read_csv(root / "ledgers" / "MASTER_21_TASK_LEDGER.csv")
    searches = read_csv(root / "ledgers" / "SEARCH_QUERY_LEDGER.csv")
    open_rows = read_csv(root / "ledgers" / "OPEN_AFTER_21_TASKS.csv")
    resolved = read_csv(root / "ledgers" / "RESOLVED_AFTER_R2_DEEP_REPLAY.csv")
    cold = json.loads((root / "qa" / "COLD_AUDIT_CHECKS.json").read_text(encoding="utf-8"))
    split_report = json.loads((root / "SPLIT_COVERAGE_REPORT.json").read_text(encoding="utf-8"))

    # The logical two-part distribution intentionally omits the original
    # 209.6 MB nested wrapper (it alone exceeded the 200 MB part ceiling) and
    # carries its twenty members byte-for-byte in an expanded directory.  The
    # split coverage report is authoritative for this one substitution.  Do
    # not generalize this exception to any other missing package-manifest row.
    replaced_wrapper = split_report.get("replaced_nested_wrapper", {})
    expected_wrapper_path = (
        "component_archives/"
        "GAL1897_CUMULATIVE_P00-P13R_REPAIRED_CANDIDATE_AND_REAUDIT.zip"
    )
    expected_wrapper_failure = f"missing:{expected_wrapper_path}"
    documented_wrapper_replacement = (
        package_failures == [expected_wrapper_failure]
        and replaced_wrapper.get("outer_member", "").endswith(expected_wrapper_path)
        and replaced_wrapper.get("size_bytes") == 209_556_731
        and replaced_wrapper.get("sha256")
        == "05C2247E2127BF816B838DA668EB9EF05AC6981D09862FB819470D79DFE3E74B"
        and replaced_wrapper.get("inner_file_count") == 20
        and str(replaced_wrapper.get("replacement_directory", "")).endswith(
            "GAL1897_CUMULATIVE_P00-P13R_REPAIRED_CANDIDATE_AND_REAUDIT_EXPANDED/"
        )
    )

    task_statuses = Counter(row["status"] for row in tasks)
    evidence_pointer_occurrences: list[dict[str, str]] = []
    for row in tasks:
        for raw_pointer in row.get("evidence_pointers", "").split(";"):
            pointer = raw_pointer.strip()
            if not pointer:
                continue
            safe_relative(pointer)
            if not (root / safe_relative(pointer)).is_file():
                evidence_pointer_occurrences.append(
                    {"task_id": row["task_id"], "pointer": pointer}
                )
    missing_pointer_names = sorted(
        {row["pointer"] for row in evidence_pointer_occurrences}
    )

    assertions = {
        "split_manifest_has_164_unique_paths": len(split_rows) == 164
        and len({row["archive_path"] for row in split_rows}) == 164,
        "all_164_split_records_replayed": not split_failures,
        "split_coverage_report_passes": split_report.get("status") == "PASS"
        and split_report.get("distributed_source_file_count") == 164,
        "package_manifest_has_142_unique_paths": len(package_rows) == 142
        and len({row["path"] for row in package_rows}) == 142,
        "package_manifest_replays_except_documented_expanded_wrapper":
        documented_wrapper_replacement,
        "critical_errata_count_is_36": len(errata) == 36,
        "dependency_edge_count_is_48": len(dependencies) == 48,
        "prior_notice_count_is_52": len(prior) == 52,
        "search_query_count_is_22": len(searches) == 22,
        "task_count_and_dispositions_are_exact": len(tasks) == 21
        and task_statuses == Counter({"repaired": 10, "proved": 9, "rejected": 2}),
        "open_set_is_exactly_three_preliminary_items": {
            row["record_id"] for row in open_rows
        }
        == {"W01-U001", "W01-U002", "W01-U003"}
        and len(open_rows) == 3,
        "r2_deep_replay_resolves_exactly_w08_and_w11": {
            row["record_id"] for row in resolved
        }
        == {"W08-WV001", "W11-U001"}
        and len(resolved) == 2,
        "cold_audit_is_242_of_242_pass": cold.get("overall_status") == "PASS"
        and cold.get("checks_passed") == 242
        and cold.get("checks_total") == 242
        and len(cold.get("checks", [])) == 242
        and all(row.get("status") == "PASS" for row in cold.get("checks", [])),
        "only_dangling_evidence_pointer_is_disclosed_open_task_file": missing_pointer_names
        == ["qa/OPEN_TASK_RESOLUTION_CHECKS.json"],
        "dangling_pointer_occurs_only_on_two_resolved_tasks": {
            row["task_id"] for row in evidence_pointer_occurrences
        }
        == {"POST-P13-A008", "W11-DA002"}
        and len(evidence_pointer_occurrences) == 2,
        "dangling_pointer_target_is_absent": not (
            root / "qa" / "OPEN_TASK_RESOLUTION_CHECKS.json"
        ).exists(),
    }

    report = {
        "schema_version": 1,
        "role": "public-safe replay receipt for the merged web R2 authority",
        "authority_identity": {
            "directory_name": root.name,
            "package_manifest_sha256": sha256(package_manifest_path),
            "split_source_manifest_sha256": sha256(split_manifest_path),
        },
        "counts": {
            "split_source_records": len(split_rows),
            "package_manifest_records": len(package_rows),
            "critical_errata": len(errata),
            "dependency_edges": len(dependencies),
            "prior_notice_records": len(prior),
            "search_queries": len(searches),
            "tasks": len(tasks),
            "open_records": len(open_rows),
            "cold_audit_checks": len(cold.get("checks", [])),
        },
        "task_status_counts": dict(sorted(task_statuses.items())),
        "open_record_ids": [row["record_id"] for row in open_rows],
        "resolved_after_r2_ids": [row["record_id"] for row in resolved],
        "split_replay_failures": split_failures,
        "package_manifest_replay_failures": package_failures,
        "package_manifest_replay_disposition": (
            "Exactly one package-manifest byte stream is absent: the original "
            "209,556,731-byte nested wrapper. The split coverage report records "
            "its exact SHA-256 and replacement by twenty byte-preserved members; "
            "all 164 distributed source records replay exactly."
        ),
        "dangling_evidence_pointers": evidence_pointer_occurrences,
        "dangling_pointer_disposition": (
            "The two task-ledger rows name qa/OPEN_TASK_RESOLUTION_CHECKS.json, "
            "but that file is absent from the R2 package. The underlying W08 and "
            "W11 evidence, certificates, source-replay files, mathematical checks, "
            "and cold-audit checks are present and hash-verified. This receipt "
            "discloses the dangling pointer and does not claim the file exists."
        ),
        "assertions": assertions,
        "result": "PASS" if all(assertions.values()) else "FAIL",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
