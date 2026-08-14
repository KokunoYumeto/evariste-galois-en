# Deterministic build and release instructions

These instructions describe the `KokunoYumeto/evariste-galois-en` release build. Publication and the reciprocal French-version update are controlled by the durable project workflow; this file never carries credentials.

## Required layout

Run from a clean copy of the English publication repository containing:

```text
source/english/GAL1897_EN_MODERN_READER.tex
source/english/tex/works/GAL1897_W01_PRELIMS.tex ... GAL1897_W11_BACKMATTER.tex
source/english/tex/wrappers/W01.tex ... W11.tex
source/english/figures/
source/french_diplomatic/
source/critical_baseline/
evidence/ENGLISH_COVERAGE.tsv
evidence/EN_FR_ALIGNMENT.tsv
evidence/GPT_CRITICAL_CALLOUTS.tsv
evidence/UNRESOLVED_ITEMS.tsv
evidence/QA_STATE.json
```

The French diplomatic and critical-baseline trees are frozen authorities. A build may read them and hash them; it must not rewrite them.

## Toolchain

Required commands:

- PowerShell 7 or Windows PowerShell 5.1;
- `latexmk` driving pdfLaTeX;
- a TeX distribution providing `babel`, `lmodern`, `microtype`, `amsmath`, `amssymb`, `array`, `graphicx`, `xcolor`, `hyperref`, `bookmark`, `tcolorbox`, and `geometry`;
- Python 3 for ledger, PDF, archive, and manifest validators;
- Poppler tools `pdfinfo`, `pdffonts`, `pdftotext`, and `pdftoppm`;
- the Python packages used by the checked-in QA scripts, recorded with exact versions in the release evidence.

Before packaging, capture `latexmk -v`, `pdflatex --version`, `python --version`, `pip freeze`, and the Poppler version strings in the evidence archive. A release must not claim a pinned/reproducible environment without that receipt.

## Non-destructive two-build procedure

The master already suppresses volatile PDF creation metadata and trailer IDs. Build it twice from identical inputs in two newly named directories that do not already exist. Never clean or reuse a directory:

```powershell
$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path -LiteralPath '.').Path
$sourceRoot = Join-Path $repoRoot 'source\english'
$stamp = Get-Date -Format 'yyyyMMddTHHmmssfff'
$pass1 = Join-Path $repoRoot "work_build\pass1-$stamp"
$pass2 = Join-Path $repoRoot "work_build\pass2-$stamp"

foreach ($target in @($pass1, $pass2)) {
  $resolvedTarget = [IO.Path]::GetFullPath($target)
  $resolvedRoot = [IO.Path]::GetFullPath($repoRoot).TrimEnd('\') + '\'
  if (-not $resolvedTarget.StartsWith($resolvedRoot, [StringComparison]::OrdinalIgnoreCase)) {
    throw "Unsafe build target outside repository: $resolvedTarget"
  }
  if (Test-Path -LiteralPath $target) { throw "Build target already exists: $target" }
  New-Item -ItemType Directory -Path $target | Out-Null
}

Push-Location -LiteralPath $sourceRoot
try {
  & latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=$pass1 GAL1897_EN_MODERN_READER.tex
  if ($LASTEXITCODE -ne 0) { throw 'Clean build pass 1 failed.' }
  & latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=$pass2 GAL1897_EN_MODERN_READER.tex
  if ($LASTEXITCODE -ne 0) { throw 'Clean build pass 2 failed.' }
} finally {
  Pop-Location
}

$pdf1 = Join-Path $pass1 'GAL1897_EN_MODERN_READER.pdf'
$pdf2 = Join-Path $pass2 'GAL1897_EN_MODERN_READER.pdf'
$hash1 = (Get-FileHash -Algorithm SHA256 -LiteralPath $pdf1).Hash
$hash2 = (Get-FileHash -Algorithm SHA256 -LiteralPath $pdf2).Hash
if ($hash1 -ne $hash2) { throw "Nondeterministic PDF builds: $hash1 != $hash2" }

$readerDir = Join-Path $repoRoot "reader-$stamp"
if (Test-Path -LiteralPath $readerDir) { throw "Release target already exists: $readerDir" }
New-Item -ItemType Directory -Path $readerDir | Out-Null
Copy-Item -LiteralPath $pdf1 -Destination (Join-Path $readerDir '00_GALOIS_1897_EN_CURRENT_LINKED_READER.pdf')
```

Recursive cleanup is prohibited for this project. Retain build directories until publication has been retrieved and verified; remove them later only through a separately audited, explicit-path operation.

## Required QA before packaging

1. Validate that W01–W11 own PDF001–PDF096 exactly once and that every English `ENSEG` identifier occurs exactly once in `evidence/EN_FR_ALIGNMENT.tsv`.
2. Re-run independent sentence/formula QA over every component. Every high/medium finding must be either repaired or retained as an explicitly unresolved release item; no finding is silently discarded.
3. Verify every source, error, witness, page-boundary, figure, and topology macro against the frozen French arguments.
4. Run `pdfinfo`, `pdffonts`, and `pdftotext -layout` against the reader. Record page count, metadata, page boxes, encryption state, bookmark/link checks, embedded-font state, and extracted-text checks.
5. Render every page with `pdftoppm -png -r 120`. Model/agent inspection must cover every page, every component seam, dense displays, critical boxes, figures, front matter, contents, colophon, and terminal blanks. Reject clipping, overlap, missing glyphs, unexpected blank/black pages, and broken links.
6. Set `evidence/QA_STATE.json` to `release_closed: true` only when the coverage, source replay, model/agent checks, deterministic build, structural checks, rendered inspection, archive tests, and manifest all pass or disclose bounded unresolved items honestly. `human_review_required` remains `false`.

Human review, sign-off, certification, community acceptance, and calendar waiting are not prerequisites.

## Release archives

Create archives with lexically sorted member paths, forward-slash member names, normalized timestamps, no duplicate names, no absolute paths, and no entries outside the declared roots. Rebuild each archive independently and require byte-identical SHA-256 values.

`01_GALOIS_1897_EN_EDITABLE_SOURCES.zip` contains the English source tree, figures, README, CITATION metadata, Zenodo metadata, license, source authority, relation sidecar, and these build instructions. Exclude auxiliary files, caches, renders, logs, credentials, and unrelated language workspaces.

`02_GALOIS_1897_EN_EVIDENCE_AND_PROVENANCE.zip` contains the complete English coverage/alignment/callout/unresolved/QA ledgers, frozen source-authority evidence, semantic/formula audit reports, structural PDF report, rendered-inspection receipt, build-environment receipt, and artifact manifests. Large private custody artifacts are represented by identifiers and hashes unless redistribution is authorized.

`OTHER_TRANSLATIONS.zip` contains the four byte-exact public files from French exact release `10.5281/zenodo.21923857` plus its public README, license, citation metadata, and Zenodo metadata under a single DOI-labelled directory:

```text
fr-10.5281-zenodo.21923857/00_GALOIS_1897_FR_CURRENT_LINKED_READER.pdf
fr-10.5281-zenodo.21923857/01_GALOIS_1897_FR_EDITABLE_SOURCES.zip
fr-10.5281-zenodo.21923857/02_GALOIS_1897_FR_EVIDENCE_AND_PROVENANCE.zip
fr-10.5281-zenodo.21923857/03_GALOIS_1897_FR_SHA256_MANIFEST.txt
fr-10.5281-zenodo.21923857/README.md
fr-10.5281-zenodo.21923857/LICENSE
fr-10.5281-zenodo.21923857/CITATION.cff
fr-10.5281-zenodo.21923857/.zenodo.json
```

The French reader hash must remain `F62D37396E04C2FC04680125E8600206FD82FA82ACE9689FF439BF30E786895A`; verify every other French member against its published manifest/receipt before nesting it.

Finally create `03_GALOIS_1897_EN_SHA256_MANIFEST.txt` containing the exact English concept/version DOIs and the filename, byte count, and uppercase SHA-256 for files `00`, `01`, `02`, and `OTHER_TRANSLATIONS.zip`. The manifest does not hash itself.

## Publication handoff

Before any GitHub push or Zenodo upload, freeze and record:

- final reader page count, bytes, and SHA-256;
- final archive bytes, CRC results, duplicate/path checks, and SHA-256 values;
- exact repository commit and tag `v2026.08.14-en-r2`;
- direct GitHub reader URL;
- exact Zenodo preview and download URLs;
- public retrieval/checksum receipts after publication.

Never read, print, log, copy, archive, commit, or upload credential contents as part of this build.
