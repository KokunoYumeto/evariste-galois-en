#!/usr/bin/env python3
"""Compare the frozen French Galois TeX topology with the English translation.

This validator deliberately ignores translated prose while requiring the source
coordinate graph, figure paths, stable ledger identifiers, environment nesting,
and mathematical material to remain aligned component by component.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


PAGE_MACROS = {
    "GalBlankTopologyPage",
    "GalCopySpecificMarkImage",
    "GalCopySpecificMarks",
    "GalExcludedSourcePage",
    "GalSourceBlankPage",
    "GalSourceImage",
    "GalSourcePageBegin",
    "GalSourcePageBoundary",
    "GalSourcePageBoundaryInWord",
    "GalSourcePageEnd",
    "GalSourcePageStart",
    "GalUnresolvedSourcePage",
    "GalVisibleFolio",
}

ISSUE_MACROS = {
    "GalControlDefect",
    "GalControlReading",
    "GalNotationAnomaly",
    "GalPrintedError",
    "GalPrintedOmission",
    "GalProofGapMark",
    "GalSourceError",
    "GalSourceErrorMark",
    "GalUnresolvedImageReading",
    "GalWitnessVariant",
}

ENVIRONMENTS = {
    "center",
    "flushleft",
    "flushright",
    "quote",
    "tabular",
    "array",
    "align*",
    "aligned",
    "split",
}

MATH_DELTA_PINS = {
    "W03": "1992F47FD5C1BCFB86BD4E2FE639AE57BAD3D9636961194E052D4A7ED9169826",
    "W05": "781FA0FAF7290CA14F703BBC6DC1931C0998DEA23652A2E98CD69E6D58A19711",
    "W06": "4D01926F28B828ED52B3B9EBAA89F282F2A3E4DB699150D457B8380AE36F126F",
    "W07": "8243F87778A9D6B35D741E41803F3E0D8533F614BAF76F43E1A82AF513F08573",
    "W08": "FCFE3140D51E748FE209A6854C461A5075880B4E6002B4BDF0822BC574007135",
    "W09": "03EB99C9E10F5AF7532756B6FFD4B816F9C9CDCAC34E03183F1485A7C9118D26",
    "W10": "4894E2B1A53B40A95816F286596283CE267CFA08225B54932EB1C86767DB4DDF",
}

# Each pin commits the complete ordered, whitespace-normalized issue-macro
# payload in both layers.  This is stronger than pinning only their set
# difference: call counts, macro names, argument counts, argument contents,
# and call order must all remain exact unless the corresponding pin is
# consciously regenerated after review.
ISSUE_DELTA_PINS = {
    "W01": "9E7E058F4342E345F0C2E08B42CA710936A56C454A9138C2D6413BBAC889CAAF",
    "W02": "CE067E888E3B0EF8C46D2F915D133260A1127FAD3F3ED5FD4BE577B420AD3E9C",
    "W03": "1F537D564CB58AF5573C5A4EF9E5ADCDE306D72A860682240270D184F0F4F63B",
    "W04": "845E3CD2DB2001BCEA9246D7557CD8418A223BDA539A9D1A551A9BE838F2231F",
    "W05": "3E49AE23E028D6DA4B55E065AECC414CB0577D0CBAFAFAB3B6B3BF43770C9FB7",
    "W06": "13C57D59A67CCE7E885DDCCCE1EF49B13F4910E4C89A3C58212CB3E6DBBEDA7D",
    "W07": "8AC288FE3BF1803547B99FC8FB2644C2EED3016D130888AB572D0DB4F01D5FD8",
    "W08": "916509C107A013C0AA2F32384913997974EE0FD26E88948BF6F4442114E43120",
    "W09": "6E7245DD89215300EA0E86190839BDD3369C0D47878782ADB7EEB73277EC41FA",
    "W10": "98697A268C331D62A35C778911B1311C22C58D95EF52F2F10BE60B0506FEDA4D",
    "W11": "ACBDB874C477B7F950C8F3AE34CDACEA6971A562D5D248691D07009F634F664F",
}

FORMULA_RECEIPTS = {
    "W03": (
        "evidence/fragments/FINAL_REAUDIT_W01_W04_W09_W11.md",
        "37C35B75E85D4D121F2A04834A6EEE3FB4AACAAA09A4ACACA7BF83991D1CF64D",
    ),
    "W05": (
        "evidence/fragments/AUDIT_W05_W08.md",
        "918CF76FE8F0A8736A3236E20015FCC82E3AF7C60686E28E77165F99F4242996",
    ),
    "W06": (
        "evidence/fragments/AUDIT_W05_W08.md",
        "918CF76FE8F0A8736A3236E20015FCC82E3AF7C60686E28E77165F99F4242996",
    ),
    "W07": (
        "evidence/fragments/AUDIT_W05_W08.md",
        "918CF76FE8F0A8736A3236E20015FCC82E3AF7C60686E28E77165F99F4242996",
    ),
    "W08": (
        "evidence/fragments/AUDIT_W05_W08.md",
        "918CF76FE8F0A8736A3236E20015FCC82E3AF7C60686E28E77165F99F4242996",
    ),
    "W09": (
        "evidence/fragments/FINAL_REAUDIT_W01_W04_W09_W11.md",
        "37C35B75E85D4D121F2A04834A6EEE3FB4AACAAA09A4ACACA7BF83991D1CF64D",
    ),
    "W10": (
        "evidence/fragments/FINAL_REAUDIT_W01_W04_W09_W11.md",
        "37C35B75E85D4D121F2A04834A6EEE3FB4AACAAA09A4ACACA7BF83991D1CF64D",
    ),
}

STABLE_ISSUE_ID = re.compile(
    r"(?:POST-P13-A\d{3}|W\d{2}-(?:PE|SE|WV|U|NA|CD)\d{3}|W1[01]-DA\d{3})"
)


def strip_comments(text: str) -> str:
    output: list[str] = []
    for line in text.splitlines(keepends=True):
        cut = len(line)
        for index, char in enumerate(line):
            if char == "%" and (index == 0 or line[index - 1] != "\\"):
                cut = index
                break
        output.append(line[:cut] + ("\n" if line.endswith("\n") and cut < len(line) else ""))
    return "".join(output)


def parse_group(text: str, start: int, opening: str = "{", closing: str = "}") -> tuple[str, int]:
    if start >= len(text) or text[start] != opening:
        raise ValueError(f"expected {opening!r} at offset {start}")
    depth = 0
    index = start
    while index < len(text):
        char = text[index]
        escaped = index > 0 and text[index - 1] == "\\"
        if not escaped:
            if char == opening:
                depth += 1
            elif char == closing:
                depth -= 1
                if depth == 0:
                    return text[start + 1 : index], index + 1
        index += 1
    raise ValueError(f"unclosed group beginning at offset {start}")


def macro_calls(text: str, names: set[str]) -> dict[str, list[list[str]]]:
    clean = strip_comments(text)
    result = {name: [] for name in names}
    pattern = re.compile(r"\\(" + "|".join(sorted(map(re.escape, names), key=len, reverse=True)) + r")(?![A-Za-z@])")
    for match in pattern.finditer(clean):
        line_start = clean.rfind("\n", 0, match.start()) + 1
        prefix = clean[line_start : match.start()]
        if "\\providecommand" in prefix or "\\newcommand" in prefix or "\\renewcommand" in prefix:
            continue
        index = match.end()
        args: list[str] = []
        while True:
            while index < len(clean) and clean[index].isspace():
                index += 1
            if index >= len(clean) or clean[index] != "{":
                break
            value, index = parse_group(clean, index)
            args.append(value)
        result[match.group(1)].append(args)
    return result


def normalize_tex(value: str) -> str:
    return re.sub(r"\s+", "", value)


def remove_macro_calls(text: str, name: str, argument_count: int) -> str:
    clean = text
    pattern = re.compile(r"\\" + re.escape(name) + r"(?![A-Za-z@])")
    cursor = 0
    pieces: list[str] = []
    while True:
        match = pattern.search(clean, cursor)
        if not match:
            pieces.append(clean[cursor:])
            break
        line_start = clean.rfind("\n", 0, match.start()) + 1
        prefix = clean[line_start : match.start()]
        if "\\providecommand" in prefix or "\\newcommand" in prefix or "\\renewcommand" in prefix:
            pieces.append(clean[cursor : match.end()])
            cursor = match.end()
            continue
        index = match.end()
        valid = True
        for _ in range(argument_count):
            while index < len(clean) and clean[index].isspace():
                index += 1
            if index >= len(clean) or clean[index] != "{":
                valid = False
                break
            _, index = parse_group(clean, index)
        if not valid:
            pieces.append(clean[cursor : match.end()])
            cursor = match.end()
            continue
        pieces.append(clean[cursor : match.start()])
        pieces.append(" ")
        cursor = index
    return "".join(pieces)


def remove_textual_math_args(value: str) -> str:
    pattern = re.compile(r"\\(?:text|textrm|textnormal|mathrm)\s*\{")
    cursor = 0
    parts: list[str] = []
    while True:
        match = pattern.search(value, cursor)
        if not match:
            parts.append(value[cursor:])
            break
        parts.append(value[cursor : match.start()])
        opening = match.end() - 1
        _, end = parse_group(value, opening)
        parts.append(match.group(0).split("{")[0] + "{<TEXT>}")
        cursor = end
    return "".join(parts)


def math_fragments(text: str) -> list[str]:
    # Critical notes are editorial additions and may contain new mathematics;
    # compare only the translated historical layer with the French authority.
    clean = strip_comments(remove_macro_calls(text, "GalCriticalNote", 2))
    fragments: list[str] = []
    index = 0
    while index < len(clean):
        if clean.startswith("\\[", index) and (index == 0 or clean[index - 1] != "\\"):
            end = clean.find("\\]", index + 2)
            while end >= 0 and end > 0 and clean[end - 1] == "\\":
                end = clean.find("\\]", end + 2)
            if end < 0:
                raise ValueError(f"unclosed \\[ at offset {index}")
            fragments.append(clean[index + 2 : end])
            index = end + 2
            continue
        if clean[index] == "$" and (index == 0 or clean[index - 1] != "\\"):
            delimiter = "$$" if clean.startswith("$$", index) else "$"
            end = clean.find(delimiter, index + len(delimiter))
            if end < 0:
                raise ValueError(f"unclosed {delimiter} at offset {index}")
            fragments.append(clean[index + len(delimiter) : end])
            index = end + len(delimiter)
            continue
        env_match = re.match(r"\\begin\{(align\*|aligned|array|split)\}", clean[index:])
        if env_match:
            env = env_match.group(1)
            content_start = index + env_match.end()
            terminator = f"\\end{{{env}}}"
            end = clean.find(terminator, content_start)
            if end < 0:
                raise ValueError(f"unclosed {env} environment at offset {index}")
            fragments.append(clean[content_start:end])
            index = end + len(terminator)
            continue
        index += 1
    return [normalize_tex(remove_textual_math_args(fragment)) for fragment in fragments]


def environment_sequence(text: str) -> list[tuple[str, str]]:
    clean = strip_comments(text)
    return [
        (kind, env)
        for kind, env in re.findall(r"\\(begin|end)\{([^}]+)\}", clean)
        if env in ENVIRONMENTS
    ]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def math_delta_digest(french: list[str], english: list[str]) -> str:
    payload = json.dumps(
        {"french": french, "english": english},
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest().upper()


def normalized_issue_calls(calls: dict[str, list[list[str]]]) -> dict[str, list[list[str]]]:
    return {
        macro: [
            [normalize_tex(argument) for argument in call]
            for call in calls[macro]
        ]
        for macro in sorted(ISSUE_MACROS)
    }


def issue_delta_digest(
    french: dict[str, list[list[str]]],
    english: dict[str, list[list[str]]],
) -> str:
    payload = json.dumps(
        {
            "french": normalized_issue_calls(french),
            "english": normalized_issue_calls(english),
        },
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest().upper()


def stable_issue_ids(calls: list[list[str]]) -> Counter[str]:
    return Counter(
        stable_id
        for call in calls
        for argument in call
        for stable_id in STABLE_ISSUE_ID.findall(argument)
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    french_dir = root / "source" / "french_diplomatic" / "tex" / "works"
    english_dir = root / "source" / "english" / "tex" / "works"

    errors: list[dict[str, object]] = []
    audited_dispositions: list[dict[str, object]] = []
    components: list[dict[str, object]] = []
    for french_path in sorted(french_dir.glob("GAL1897_W*.tex")):
        english_path = english_dir / french_path.name
        item: dict[str, object] = {
            "component": french_path.name.split("_")[1],
            "french": french_path.relative_to(root).as_posix(),
            "english": english_path.relative_to(root).as_posix(),
            "french_sha256": digest(french_path),
        }
        if not english_path.exists():
            errors.append({"component": item["component"], "kind": "missing_english_file"})
            components.append(item)
            continue

        french = french_path.read_text(encoding="utf-8")
        english = english_path.read_text(encoding="utf-8")
        item["english_sha256"] = digest(english_path)

        page_fr = macro_calls(french, PAGE_MACROS)
        page_en = macro_calls(english, PAGE_MACROS)
        for macro in sorted(PAGE_MACROS):
            left = [[normalize_tex(arg) for arg in call] for call in page_fr[macro]]
            right = [[normalize_tex(arg) for arg in call] for call in page_en[macro]]
            if left != right:
                # W01's unresolved page embeds its rendered witness note inside
                # argument 4.  The English layer adds only the frozen stable ID
                # to that note; arguments 1--3 and the source payload otherwise
                # remain identical.  Record this audited apparatus-only delta.
                w01_id_only = (
                    item["component"] == "W01"
                    and macro == "GalUnresolvedSourcePage"
                    and len(left) == len(right) == 1
                    and left[0][:3] == right[0][:3]
                    and right[0][3].replace("\\textbf{W01-U002---unresolvedtopology.}", "") == left[0][3]
                )
                if w01_id_only:
                    audited_dispositions.append({
                        "component": "W01",
                        "kind": "page_macro_apparatus_only_delta",
                        "macro": macro,
                        "disposition": "PASS: stable unresolved ID added to embedded witness note; coordinates and payload preserved",
                    })
                else:
                    errors.append({
                        "component": item["component"],
                        "kind": "page_macro_mismatch",
                        "macro": macro,
                        "french": left,
                        "english": right,
                    })

        issue_fr = macro_calls(french, ISSUE_MACROS)
        issue_en = macro_calls(english, ISSUE_MACROS)
        issue_counts_fr = {
            macro: len(issue_fr[macro])
            for macro in sorted(ISSUE_MACROS)
            if issue_fr[macro] or issue_en[macro]
        }
        issue_counts_en = {
            macro: len(issue_en[macro])
            for macro in sorted(ISSUE_MACROS)
            if issue_fr[macro] or issue_en[macro]
        }
        for macro in sorted(ISSUE_MACROS):
            french_count = len(issue_fr[macro])
            english_count = len(issue_en[macro])
            # The English edition may add explicit marker macros at claims that
            # the diplomatic source only diagnoses in an external ledger, but
            # it may never contain fewer calls of a macro than the source.
            if english_count < french_count:
                errors.append({
                    "component": item["component"],
                    "kind": "issue_macro_call_count_loss",
                    "macro": macro,
                    "french_count": french_count,
                    "english_count": english_count,
                })

            # Stable IDs already present in the diplomatic source remain a
            # separate non-negotiable invariant.  Count duplicate uses too.
            missing_ids = (
                stable_issue_ids(issue_fr[macro])
                - stable_issue_ids(issue_en[macro])
            )
            if missing_ids:
                errors.append({
                    "component": item["component"],
                    "kind": "stable_issue_id_loss",
                    "macro": macro,
                    "missing_ids": [
                        {"stable_id": stable_id, "count": count}
                        for stable_id, count in sorted(missing_ids.items())
                    ],
                })

        component = str(item["component"])
        observed_issue_delta = issue_delta_digest(issue_fr, issue_en)
        expected_issue_delta = ISSUE_DELTA_PINS.get(component)
        if observed_issue_delta == expected_issue_delta:
            audited_dispositions.append({
                "component": component,
                "kind": "hash_pinned_issue_call_delta",
                "issue_macro_calls_french": sum(issue_counts_fr.values()),
                "issue_macro_calls_english": sum(issue_counts_en.values()),
                "issue_macro_counts_french": issue_counts_fr,
                "issue_macro_counts_english": issue_counts_en,
                "delta_sha256": observed_issue_delta,
                "disposition": "PASS: complete ordered normalized issue-call payload matches its frozen per-component pin",
            })
        else:
            errors.append({
                "component": component,
                "kind": "unpinned_or_changed_issue_call_delta",
                "issue_macro_counts_french": issue_counts_fr,
                "issue_macro_counts_english": issue_counts_en,
                "observed_delta_sha256": observed_issue_delta,
                "expected_delta_sha256": expected_issue_delta,
            })

        env_fr = environment_sequence(french)
        env_en = environment_sequence(english)
        if env_fr != env_en:
            errors.append({
                "component": item["component"],
                "kind": "environment_sequence_mismatch",
                "french": env_fr,
                "english": env_en,
            })

        math_fr = math_fragments(french)
        math_en = math_fragments(english)
        if math_fr != math_en:
            first = next(
                (index for index, pair in enumerate(zip(math_fr, math_en)) if pair[0] != pair[1]),
                min(len(math_fr), len(math_en)),
            )
            component = str(item["component"])
            delta_digest = math_delta_digest(math_fr, math_en)
            receipt_spec = FORMULA_RECEIPTS.get(component)
            pin = MATH_DELTA_PINS.get(component)
            receipt_ok = False
            receipt_path = None
            receipt_digest = None
            if receipt_spec:
                receipt_path = root / receipt_spec[0]
                receipt_digest = digest(receipt_path) if receipt_path.is_file() else None
                receipt_ok = receipt_digest == receipt_spec[1]
            if pin == delta_digest and receipt_ok:
                audited_dispositions.append({
                    "component": component,
                    "kind": "hash_pinned_math_fragment_delta",
                    "first_mismatch": first,
                    "french_count": len(math_fr),
                    "english_count": len(math_en),
                    "delta_sha256": delta_digest,
                    "disposition": "PASS: exact normalized delta matches its frozen pin and the independent formula-audit receipt hash matches",
                    "receipt": receipt_spec[0],
                    "receipt_sha256": receipt_digest,
                })
            else:
                errors.append({
                    "component": component,
                    "kind": "unpinned_or_changed_math_sequence_mismatch",
                    "first_mismatch": first,
                    "french_count": len(math_fr),
                    "english_count": len(math_en),
                    "observed_delta_sha256": delta_digest,
                    "expected_delta_sha256": pin,
                    "receipt": receipt_spec[0] if receipt_spec else None,
                    "receipt_exists": bool(receipt_path and receipt_path.is_file()),
                    "observed_receipt_sha256": receipt_digest,
                    "expected_receipt_sha256": receipt_spec[1] if receipt_spec else None,
                    "french_fragment": math_fr[first] if first < len(math_fr) else None,
                    "english_fragment": math_en[first] if first < len(math_en) else None,
                })

        item.update({
            "page_macro_calls": sum(map(len, page_fr.values())),
            "issue_macro_calls_french": sum(map(len, issue_fr.values())),
            "issue_macro_calls_english": sum(map(len, issue_en.values())),
            "issue_call_delta_sha256": observed_issue_delta,
            "math_fragments_french": len(math_fr),
            "math_fragments_english": len(math_en),
            "environment_events": len(env_fr),
            "enseg_markers": len(re.findall(r"(?m)^\s*%\s*ENSEG:", english)),
        })
        components.append(item)

    observed_component_counts = Counter(
        str(item["component"]) for item in components
    )
    expected_component_counts = Counter(ISSUE_DELTA_PINS.keys())
    if observed_component_counts != expected_component_counts:
        errors.append({
            "kind": "issue_delta_pin_component_set_mismatch",
            "missing_components": sorted(
                (expected_component_counts - observed_component_counts).elements()
            ),
            "unexpected_or_duplicate_components": sorted(
                (observed_component_counts - expected_component_counts).elements()
            ),
        })

    report = {
        "schema_version": 1,
        "root": ".",
        "components": components,
        "audited_dispositions": audited_dispositions,
        "errors": errors,
        "pass": not errors,
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
