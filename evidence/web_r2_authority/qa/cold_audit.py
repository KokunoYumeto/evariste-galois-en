#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from collections import Counter
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
CHECKS: list[dict] = []


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest().upper()


def add(check_id: str, category: str, description: str, passed: bool, detail=None) -> None:
    CHECKS.append({
        'check_id': check_id,
        'category': category,
        'description': description,
        'status': 'PASS' if passed else 'FAIL',
        'detail': detail,
    })


def read_csv(rel: str) -> list[dict]:
    p = ROOT / rel
    with p.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def check_zip_crc(check_id: str, path: Path, category: str = 'archive') -> None:
    try:
        with zipfile.ZipFile(path) as zf:
            bad = zf.testzip()
        add(check_id, category, f'ZIP CRC succeeds: {path.name}', bad is None, bad)
    except Exception as exc:
        add(check_id, category, f'ZIP CRC succeeds: {path.name}', False, repr(exc))


# Required tree and immutable component.
required = [
    'README.md', 'RETURN_TO_CODEX.md', 'BLOCKERS.md',
    'component_archives/GAL1897_CUMULATIVE_P00-P13R_REPAIRED_CANDIDATE_AND_REAUDIT.zip',
    'frozen_diplomatic/GAL1897_1897_SOURCE_FAITHFUL_CANDIDATE_P13R_AUDIT_BUILD.pdf',
    'critical_edition/GAL1897_GPT_CRITICAL_EDITION.md',
    'critical_edition/GAL1897_GPT_CRITICAL_EDITION.tex',
    'critical_edition/GAL1897_GPT_CRITICAL_EDITION.pdf',
    'critical_edition/GAL1897_ONE_CLICK_READER_DIPLOMATIC_PLUS_GPT_CRITICAL.pdf',
    'ledgers/MASTER_21_TASK_LEDGER.csv',
    'ledgers/CRITICAL_ERRATA_CATALOGUE.csv',
    'ledgers/BIBLIOGRAPHIC_PRIOR_NOTICE_MATRIX.csv',
    'ledgers/DEPENDENCY_PROPAGATION_EDGES.csv',
    'ledgers/SEARCH_QUERY_LEDGER.csv',
    'ledgers/OPEN_AFTER_21_TASKS.csv',
    'ledgers/RESOLVED_AFTER_R2_DEEP_REPLAY.csv',
    'qa/MATHEMATICAL_CHECKS.json', 'qa/PDF_PIXEL_REPLAY.json',
    'qa/RENDERER_PARITY_SUMMARY.json', 'qa/DETERMINISTIC_BUILD_RECEIPT.json',
]
for n, rel in enumerate(required, 1):
    add(f'TREE-{n:03d}', 'tree', f'Required payload exists: {rel}', (ROOT / rel).is_file(), rel)

component = ROOT / 'component_archives/GAL1897_CUMULATIVE_P00-P13R_REPAIRED_CANDIDATE_AND_REAUDIT.zip'
component_expected = '05C2247E2127BF816B838DA668EB9EF05AC6981D09862FB819470D79DFE3E74B'
add('IMM-001', 'immutability', 'P13R cumulative handoff hash is unchanged', sha256(component) == component_expected, sha256(component))
sidecar = ROOT / 'component_archives/GAL1897_CUMULATIVE_P00-P13R_REPAIRED_CANDIDATE_AND_REAUDIT.zip.sha256'
add('IMM-002', 'immutability', 'P13R handoff sidecar contains governing hash', component_expected in sidecar.read_text(encoding='utf-8'), sidecar.read_text(encoding='utf-8').strip())
check_zip_crc('IMM-003', component, 'immutability')

frozen = ROOT / 'frozen_diplomatic/GAL1897_1897_SOURCE_FAITHFUL_CANDIDATE_P13R_AUDIT_BUILD.pdf'
frozen_expected = '8E6071A2E4A0D38CC89232553CE0CC0314C7EF4BD0A084240C41D60B0AEBBFC5'
add('IMM-004', 'immutability', 'Frozen diplomatic PDF hash is unchanged', sha256(frozen) == frozen_expected, sha256(frozen))
try:
    frozen_pages = len(PdfReader(str(frozen)).pages)
except Exception:
    frozen_pages = -1
add('IMM-005', 'immutability', 'Frozen diplomatic PDF has 78 pages', frozen_pages == 78, frozen_pages)

# Original source packet, manifest hashes, mappings, and ZIP CRC.
packet = ROOT / 'original_source_packet'
packet_files = sorted(p for p in packet.iterdir() if p.is_file())
add('SRC-000', 'source_packet', 'Original packet contains 36 files including manifest', len(packet_files) == 36, len(packet_files))
manifest = packet / '23_PACKET_MANIFEST_SHA256.txt'
manifest_rows: list[tuple[str, str]] = []
for line in manifest.read_text(encoding='utf-8').splitlines():
    m = re.match(r'^([0-9A-F]{64}) \*(.+)$', line)
    if m:
        manifest_rows.append((m.group(2), m.group(1)))
add('SRC-001', 'source_packet', 'Packet manifest contains 35 payload hashes', len(manifest_rows) == 35, len(manifest_rows))
for i, (name, expected) in enumerate(manifest_rows, 1):
    p = packet / name
    actual = sha256(p) if p.is_file() else None
    add(f'SRC-HASH-{i:03d}', 'source_packet', f'Packet payload hash matches: {name}', actual == expected, actual)

# All packet ZIPs are readable and CRC-valid.
for i, zp in enumerate(sorted(packet.glob('*.zip')), 1):
    check_zip_crc(f'SRC-ZIP-{i:03d}', zp, 'source_packet')

page_map = read_csv('original_source_packet/04_GALOIS_1897_PAGE_MAP.csv')
pages = [int(r['pdf_page1']) for r in page_map]
leaves = [r['jp2_leaf'] for r in page_map]
add('MAP-001', 'mapping', 'Page map has exactly 96 rows', len(page_map) == 96, len(page_map))
add('MAP-002', 'mapping', 'Physical pages are exactly 1-96', sorted(pages) == list(range(1, 97)) and len(set(pages)) == 96, [min(pages), max(pages), len(set(pages))])
add('MAP-003', 'mapping', 'JP2 leaves are exactly L0000-L0095', sorted(leaves) == [f'L{i:04d}' for i in range(96)] and len(set(leaves)) == 96, [leaves[0], leaves[-1], len(set(leaves))])
image_inventory = read_csv('original_source_packet/05_JP2_IMAGE_INVENTORY_SHA256.csv')
add('MAP-004', 'mapping', 'JP2 inventory has 96 unique leaves', len(image_inventory) == 96 and len({int(r['jp2_leaf_index0']) for r in image_inventory}) == 96, len(image_inventory))
archive_map = read_csv('original_source_packet/06_JP2_ARCHIVE_MAP.csv')
add('MAP-005', 'mapping', 'JP2 archive map has 14 bounded archives', len(archive_map) == 14, len(archive_map))
add('MAP-006', 'mapping', 'JP2 archive image counts sum to 96', sum(int(r['image_count']) for r in archive_map) == 96, sum(int(r['image_count']) for r in archive_map))

source_authority = read_csv('evidence/SOURCE_AUTHORITY_MANIFEST.csv')
add('AUTH-001', 'authority', 'Source-authority manifest has 36 rows', len(source_authority) == 36, len(source_authority))
add('AUTH-002', 'authority', 'Every inventoried source is accessible', all(r['accessible'] == 'yes' for r in source_authority), sorted(set(r['accessible'] for r in source_authority)))
add('AUTH-003', 'authority', 'Authority classes are restricted to primary/secondary/control', set(r['authority_class'] for r in source_authority) <= {'primary', 'secondary', 'control_or_governance'}, sorted(set(r['authority_class'] for r in source_authority)))

# Master 21-task ledger and per-task certificates.
expected_status = {
    'POST-P13-A001':'repaired','POST-P13-A002':'proved','POST-P13-A003':'proved','POST-P13-A004':'proved',
    'POST-P13-A005':'rejected','POST-P13-A006':'repaired','POST-P13-A007':'proved','POST-P13-A008':'repaired',
    'POST-P13-A009':'proved','POST-P13-A010':'repaired','POST-P13-A011':'repaired','POST-P13-A012':'repaired',
    'POST-P13-A013':'repaired','POST-P13-A014':'proved','W10-DA001':'repaired','W10-DA002':'repaired',
    'W10-DA003':'rejected','W10-DA004':'repaired','W11-DA001':'proved','W11-DA002':'proved','W11-DA003':'proved',
}
master = read_csv('ledgers/MASTER_21_TASK_LEDGER.csv')
master_by_id = {r['task_id']: r for r in master}
add('TASK-000', 'tasks', 'Master ledger contains exactly 21 unique task IDs', len(master) == 21 and len(master_by_id) == 21 and set(master_by_id) == set(expected_status), sorted(master_by_id))
add('TASK-001', 'tasks', 'Disposition count is 10 repaired, 9 proved, 2 rejected', Counter(r['status'] for r in master) == Counter({'repaired':10,'proved':9,'rejected':2}), dict(Counter(r['status'] for r in master)))
add('TASK-002', 'tasks', 'No 21-task row remains unresolved', all(r['status'] != 'unresolved_after_bounded_search' for r in master), [r['task_id'] for r in master if 'unresolved' in r['status']])
for i, (task_id, status) in enumerate(expected_status.items(), 1):
    row = master_by_id.get(task_id)
    add(f'TASK-STATUS-{i:03d}', 'tasks', f'{task_id} has frozen R2 status {status}', row is not None and row['status'] == status, row['status'] if row else None)
    cert = ROOT / f'certificates/{task_id}.md'
    cert_text = cert.read_text(encoding='utf-8') if cert.is_file() else ''
    add(f'TASK-CERT-{i:03d}', 'tasks', f'{task_id} certificate exists and states status {status}', cert.is_file() and f'**Status:** {status}' in cert_text, str(cert.relative_to(ROOT)) if cert.is_file() else None)

# All 36 errata close in critical layer without diplomatic mutation.
errata = read_csv('ledgers/CRITICAL_ERRATA_CATALOGUE.csv')
errata_ids = [r['error_id'] for r in errata]
add('ERR-000', 'errata', 'Critical errata catalogue has 36 unique rows', len(errata) == 36 and len(set(errata_ids)) == 36, len(errata))
for i, r in enumerate(errata, 1):
    passed = r['diplomatic_layer_mutated'] == 'no' and r['critical_layer_state'] == 'closed' and bool(r['proof_certificate'].strip())
    add(f'ERR-{i:03d}', 'errata', f"{r['error_id']} is closed only in the critical layer", passed, {'adjudication':r['adjudication'],'diplomatic_layer_mutated':r['diplomatic_layer_mutated']})

# Structured companions.
prop = read_csv('ledgers/DEPENDENCY_PROPAGATION_EDGES.csv')
add('LEDGER-001', 'ledgers', 'Dependency/propagation ledger has 48 edges', len(prop) == 48, len(prop))
add('LEDGER-002', 'ledgers', 'Every propagation edge has source, target, outcome, and certificate', all(all(r[k].strip() for k in ['source_id','target_id_or_scope','propagation_outcome','certificate']) for r in prop), None)
prior = read_csv('ledgers/BIBLIOGRAPHIC_PRIOR_NOTICE_MATRIX.csv')
add('LEDGER-003', 'ledgers', 'Prior-notice matrix has 52 rows', len(prior) == 52, len(prior))
add('LEDGER-004', 'ledgers', 'Prior-notice matrix includes all 36 errata IDs', set(errata_ids) <= {r['record_id'] for r in prior}, sorted(set(errata_ids)-{r['record_id'] for r in prior}))
search = read_csv('ledgers/SEARCH_QUERY_LEDGER.csv')
add('LEDGER-005', 'ledgers', 'Search ledger has 22 dated query rows', len(search) == 22 and len({r['query_id'] for r in search}) == 22, len(search))
open_rows = read_csv('ledgers/OPEN_AFTER_21_TASKS.csv')
add('LEDGER-006', 'ledgers', 'Only three inherited W01 records remain open', {r['record_id'] for r in open_rows} == {'W01-U001','W01-U002','W01-U003'}, [r['record_id'] for r in open_rows])
resolved = read_csv('ledgers/RESOLVED_AFTER_R2_DEEP_REPLAY.csv')
add('LEDGER-007', 'ledgers', 'R2 resolution ledger closes exactly W08-WV001 and W11-U001', {r['record_id'] for r in resolved} == {'W08-WV001','W11-U001'} and all(r['diplomatic_layer_mutated'] == 'false' for r in resolved), resolved)
variants = read_csv('ledgers/R2_WITNESS_VARIANT_ADJUDICATIONS.csv')
add('LEDGER-008', 'ledgers', 'R2 witness-variant adjudication ledger is present', len(variants) >= 1 and any((r.get('variant_id') or r.get('record_id')) == 'W08-WV001' for r in variants), len(variants))

# R2 deep replay: Tannery formula and ETH printer number.
a008 = (ROOT / 'certificates/POST-P13-A008.md').read_text(encoding='utf-8')
w11 = (ROOT / 'certificates/W11-DA002.md').read_text(encoding='utf-8')
add('R2-A008-001', 'deep_replay', 'Tannery first manuscript glyph is adjudicated as E', 'first letter of the manuscript formula has three horizontal strokes and is **E**' in a008, None)
add('R2-A008-002', 'deep_replay', 'Correct determinant formula is recorded', "E'F''-E''F'" in a008 or 'E′F″-E″F′' in a008, None)
add('R2-A008-003', 'deep_replay', 'Equivalence proof includes explicit period normalization', all(t in a008 for t in ['omega_1=F','omega_2=iF_c','eta_1=E','eta_2=i(F_c-E_c)']), None)
add('R2-A008-004', 'deep_replay', 'Admissibility of second-kind period vector is justified', 'Riemann bilinear relation' in a008 and 'Adding $c$ times the holomorphic first-kind differential' in a008, None)
add('R2-A008-005', 'deep_replay', 'Tannery formula evidence figure exists', (ROOT/'evidence/figures/POST_P13_A008_TANNERY_READING.png').is_file(), None)
add('R2-W11-001', 'deep_replay', 'Printer number is recorded as five-digit 24572', '24572' in w11 and 'five digits, not four' in w11, None)
add('R2-W11-002', 'deep_replay', 'ETH comparison figure exists', (ROOT/'evidence/figures/W11_DA002_JOB_NUMBER_COMPARISON.png').is_file(), None)
eth_pdf = ROOT/'evidence/source_replay/ETH_Rar4575_Galois1897.pdf'
eth_ocr = ROOT/'evidence/source_replay/ETH_Rar4575_Galois1897_OCR.txt'
add('R2-W11-003', 'deep_replay', 'ETH Rar 4575 PDF hash matches receipt', sha256(eth_pdf) == '30313C4A4C8966E548FD065A3FE220B0F36984617CD0FF3C210CD7971007F732', sha256(eth_pdf))
add('R2-W11-004', 'deep_replay', 'ETH OCR hash matches receipt', sha256(eth_ocr) == '5BD69EE3B9758EE50C7E04C123D60148500C4BFF918F02B85EAB0EE32FDE1BD0', sha256(eth_ocr))
add('R2-W11-005', 'deep_replay', 'ETH OCR contains printer number 24572', '24572' in eth_ocr.read_text(encoding='utf-8', errors='replace'), None)
add('R2-W11-006', 'deep_replay', 'ETH PDF has page-level comparison coverage', len(PdfReader(str(eth_pdf)).pages) == 83, len(PdfReader(str(eth_pdf)).pages))
add('R2-W11-007', 'deep_replay', 'Independent ETH table-of-contents render is included', (ROOT/'evidence/source_replay/ETH_1897_TABLE_OF_CONTENTS.png').is_file(), None)

# Source-replay hash manifest.
replay_manifest = ROOT/'evidence/source_replay/SOURCE_REPLAY_SHA256.txt'
replay_rows=[]
for line in replay_manifest.read_text(encoding='ascii').splitlines():
    m=re.match(r'^([0-9A-F]{64})  (.+)$',line)
    if m: replay_rows.append((m.group(2),m.group(1)))
add('REPLAY-000','deep_replay','Source-replay hash manifest has 17 entries',len(replay_rows)==17,len(replay_rows))
for i,(rel,expected) in enumerate(replay_rows,1):
    p=ROOT/rel
    actual=sha256(p) if p.is_file() else None
    add(f'REPLAY-{i:03d}','deep_replay',f'Source-replay hash matches: {rel}',actual==expected,actual)

# Mathematical and deterministic-build receipts.
math = json.loads((ROOT/'qa/MATHEMATICAL_CHECKS.json').read_text(encoding='utf-8'))
add('MATH-001','mathematics','Mathematical checks report PASS 12/12', math.get('status')=='PASS' and math.get('checks_passed')==12 and math.get('checks_total')==12, math)
for i,c in enumerate(math.get('checks',[]),1):
    add(f'MATH-{i+1:03d}','mathematics',c.get('check_id','mathematical check'),c.get('status')=='PASS',c.get('detail'))
build_receipt=json.loads((ROOT/'qa/DETERMINISTIC_BUILD_RECEIPT.json').read_text(encoding='utf-8'))
add('BUILD-001','build','Two independent critical builds are byte-identical',build_receipt.get('critical_byte_identical') is True and build_receipt.get('critical_build_a_sha256')==build_receipt.get('critical_build_b_sha256'),build_receipt.get('critical_build_a_sha256'))
add('BUILD-002','build','Two independent reader merges are byte-identical',build_receipt.get('reader_byte_identical') is True and build_receipt.get('reader_build_a_sha256')==build_receipt.get('reader_build_b_sha256'),build_receipt.get('reader_build_a_sha256'))

critical = ROOT/'critical_edition/GAL1897_GPT_CRITICAL_EDITION.pdf'
reader = ROOT/'critical_edition/GAL1897_ONE_CLICK_READER_DIPLOMATIC_PLUS_GPT_CRITICAL.pdf'
critical_hash=sha256(critical); reader_hash=sha256(reader)
add('PDF-001','pdf','Critical PDF hash agrees with build receipt',critical_hash==build_receipt.get('final_critical_pdf_sha256'),critical_hash)
add('PDF-002','pdf','Reader PDF hash agrees with build receipt',reader_hash==build_receipt.get('final_reader_pdf_sha256'),reader_hash)
try: cp=len(PdfReader(str(critical)).pages)
except Exception: cp=-1
try: rp=len(PdfReader(str(reader)).pages)
except Exception: rp=-1
add('PDF-003','pdf','Critical appendix has 24 pages',cp==24,cp)
add('PDF-004','pdf','One-click reader has 102 pages',rp==102,rp)

pixel=json.loads((ROOT/'qa/PDF_PIXEL_REPLAY.json').read_text(encoding='utf-8'))
add('PDF-005','pdf','Poppler and PDFium both preserve 78/78 diplomatic prefix pages and 24/24 appendix pages',pixel.get('overall_pass') is True and all(e.get('prefix_passed')==78 and e.get('append_passed')==24 for e in pixel.get('engines',[])),[(e.get('engine'),e.get('prefix_passed'),e.get('append_passed')) for e in pixel.get('engines',[])])
parity=json.loads((ROOT/'qa/RENDERER_PARITY_SUMMARY.json').read_text(encoding='utf-8'))
add('PDF-006','pdf','Critical appendix passes 24-page renderer-parity bounding-box test',parity.get('overall_pass') is True and parity.get('passed')==24,{'passed':parity.get('passed'),'max_bbox_difference_px':parity.get('max_bbox_difference_px')})
for rel,cid in [('qa/PDF_PREFLIGHT_CRITICAL.json','PDF-007'),('qa/PDF_PREFLIGHT_READER.json','PDF-008')]:
    q=json.loads((ROOT/rel).read_text(encoding='utf-8'))
    add(cid,'pdf',f'{rel} reports openable unencrypted PDF with no warnings',q.get('ok_open') is True and q.get('encrypted') is False and not q.get('warnings'),q)

# Font embedding and Ghostscript preflight.
def embedded_fonts(rel: str) -> tuple[bool,list[str]]:
    lines=(ROOT/rel).read_text(encoding='utf-8').splitlines()[2:]
    bad=[]
    for line in lines:
        cols=line.split()
        if len(cols)>=6 and cols[5] != 'yes': bad.append(line)
    return not bad,bad
ok,bad=embedded_fonts('qa/PDFFONTS_CRITICAL.txt'); add('PDF-009','pdf','All critical-PDF fonts are embedded',ok,bad)
ok,bad=embedded_fonts('qa/PDFFONTS_READER.txt'); add('PDF-010','pdf','All reader-PDF fonts are embedded',ok,bad)
add('PDF-011','pdf','Ghostscript preflight succeeds for critical PDF',(ROOT/'qa/GHOSTSCRIPT_CRITICAL.txt').read_text(encoding='utf-8').strip()=='',(ROOT/'qa/GHOSTSCRIPT_CRITICAL.txt').read_text(encoding='utf-8').strip())
add('PDF-012','pdf','Ghostscript preflight succeeds for reader PDF',(ROOT/'qa/GHOSTSCRIPT_READER.txt').read_text(encoding='utf-8').strip()=='',(ROOT/'qa/GHOSTSCRIPT_READER.txt').read_text(encoding='utf-8').strip())

# TeX/source structural and visible-text checks.
md=(ROOT/'critical_edition/GAL1897_GPT_CRITICAL_EDITION.md').read_text(encoding='utf-8')
tex=(ROOT/'critical_edition/GAL1897_GPT_CRITICAL_EDITION.tex').read_text(encoding='utf-8')
add('STRUCT-001','structure','Markdown headings are separated from preceding blocks',all(i==0 or not lines[i-1].strip() for lines in [md.splitlines()] for i,l in enumerate(lines) if l.startswith('#')),None)
add('STRUCT-002','structure','Generated TeX has balanced begin/end environment counts',len(re.findall(r'\\begin\{[^}]+\}',tex))==len(re.findall(r'\\end\{[^}]+\}',tex)),[len(re.findall(r'\\begin\{[^}]+\}',tex)),len(re.findall(r'\\end\{[^}]+\}',tex))])
control=[]
for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.md','.txt','.csv','.json','.tex','.py','.sh'} and 'provenance/surviving_predecessor_files' not in p.as_posix() and not any(part.startswith('_build') for part in p.parts):
        try: s=p.read_text(encoding='utf-8')
        except Exception: continue
        if any(ord(c)<32 and c not in '\n\r\t' for c in s): control.append(p.relative_to(ROOT).as_posix())
add('STRUCT-003','structure','Active textual payload contains no illicit control characters',not control,control)
critical_text='\n'.join((p.extract_text() or '') for p in PdfReader(str(critical)).pages)
add('STRUCT-004','structure','Rendered critical PDF contains no leaked Markdown heading markers','##' not in critical_text,None)
add('STRUCT-005','structure','Rendered critical PDF states both R2 resolutions','24572' in critical_text and ('E′F″' in critical_text or "E'F''" in critical_text),None)
add('STRUCT-006','structure','Active master files do not retain old 22-page/100-page artifact claims','22-page critical PDF' not in md and '100-page one-click reader' not in md,None)

# Provenance of the unavailable predecessor is preserved without false identity claim.
incident=(ROOT/'provenance/MISSING_PREDECESSOR_ZIP_INCIDENT.md').read_text(encoding='utf-8')
add('PROV-001','provenance','Missing predecessor incident explicitly rejects byte-identity claim','does **not** claim byte identity' in incident,None)
add('PROV-002','provenance','Predecessor sidecar survives as provenance',(ROOT/'provenance/missing_predecessor_archive/GAL1897_CUMULATIVE_P00-P13R_POST_P13_GPT_CRITICAL_EDITION_21_TASKS.zip.sha256').is_file(),None)
add('PROV-003','provenance','Predecessor package receipt survives as provenance',(ROOT/'provenance/missing_predecessor_archive/GAL1897_POST_P13_GPT_CRITICAL_EDITION_21_TASKS_PACKAGE_RECEIPT.json').is_file(),None)

failures=[c for c in CHECKS if c['status']!='PASS']
result={
    'generated':'2026-08-14',
    'artifact':'GAL1897_POST_P13_GPT_CRITICAL_EDITION_21_TASKS_R2',
    'overall_status':'PASS' if not failures else 'FAIL',
    'checks_passed':len(CHECKS)-len(failures),
    'checks_total':len(CHECKS),
    'failures':failures,
    'checks':CHECKS,
}
(ROOT/'qa/COLD_AUDIT_CHECKS.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
report=[
    '# Independent R2 cold audit', '',
    f"**Overall result: {result['overall_status']} — {result['checks_passed']}/{result['checks_total']} checks passed.**", '',
]
if failures:
    report += ['## Failures',''] + [f"- `{c['check_id']}`: {c['description']} — {c['detail']}" for c in failures] + ['']
else:
    report += [
        'No blocking defect remains in the reconstructed successor package.', '',
        'The audit independently re-inventoried the immutable P13R handoff, the complete original source packet, all 21 task dispositions and certificates, all 36 critical errata records, the 52-row provenance matrix, the propagation and search ledgers, the two R2 deep-replay resolutions, mathematical checks, deterministic builds, PDF structure, two-renderer pixel replay, and the missing-predecessor provenance record.', '',
        'The 21-task disposition is 10 repaired, 9 proved, 2 rejected, and 0 unresolved. The only open records are W01-U001, W01-U002, and W01-U003, all outside the 21-task scope.', '',
    ]
report += [
    '## Active PDF hashes','',
    f'- Critical appendix: `{critical_hash}` ({cp} pages).',
    f'- One-click reader: `{reader_hash}` ({rp} pages).',
    f'- Frozen diplomatic prefix: `{sha256(frozen)}` ({frozen_pages} pages).','',
    '## Publication constraint','',
    'This package is a proposed integration handoff. It does not mutate the frozen diplomatic edition and does not perform a DOI, Zenodo, or GitHub publication action.','',
]
(ROOT/'qa/COLD_AUDIT_REPORT.md').write_text('\n'.join(report),encoding='utf-8')
print(json.dumps({'overall_status':result['overall_status'],'checks_passed':result['checks_passed'],'checks_total':result['checks_total'],'failure_ids':[c['check_id'] for c in failures]},indent=2))
raise SystemExit(0 if not failures else 1)
