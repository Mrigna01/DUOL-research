# Duolingo Valuation and Investment Research

This project contains a five-year DUOL financial model, interactive valuation workbench, research evolution, investment memo and validation evidence. Original labs remain in the parent repository; Superseded packages and ZIPs are preserved outside the repository at C:/Users/mrign/Documents/DUOL-not-for-submission-20261018/.

**Recommendation: Watch / Defer.** September 21, 2026 valuation: base **$137.57**, causal low/base/high **$114.20 / $137.57 / $165.01**, versus dated market **$149.42**. USD millions except per-share value; 50.7m diluted valuation shares. Intended audience: buy-side committee with no existing position. Investment horizon: 3-5 years. These are conditional estimates, not probabilities or a current quote.

## What to open

- [Visible executed report](outputs/visible-output.html): all material results, statements, assumptions links and checks without running code.
- [Decision-Memo.pdf](docs/Decision-Memo.pdf): two-page decision and conditions.
- [Research-Evolution.pdf](docs/Research-Evolution.pdf): original investment thesis, research development and model revisions.
- [Validation-and-AI-Use.pdf](docs/Validation-and-AI-Use.pdf): executed tests, AI-use disclosure and evidence limitations.
- [Existing Locked Record reconciliation](docs/locked-changed-input-record.md): preserves both original and later Lab 11 versions.
- [Submission manifest](submission-manifest.csv): deliverables, recording status and access checks.

## Run - no package installation for the model or panel

Use Python 3.13; the exact cold-run interpreter version is recorded in evidence/cold-environment.txt. Open a terminal in this folder:

```powershell
python -B analysis.py
python -B validate.py --panel
python -B panel.py
```

Open **http://127.0.0.1:8765**. Stop with Ctrl+C. If needed, use `python -B panel.py --port 8766`. The automated panel tests temporarily use port 18765; it must be free. The analysis writes generated CSV/JSON and the HTML report under outputs/. No live API keys, accounts, network requests or notebooks are needed. The raw evidence is local. The `-B` flag prevents generated Python cache files.

To rebuild the three PDFs after editing their Markdown sources:

```powershell
python -m venv "$env:TEMP\fin439-project1-pdf-env"
& "$env:TEMP\fin439-project1-pdf-env\Scripts\python.exe" -m pip install -r requirements.txt
& "$env:TEMP\fin439-project1-pdf-env\Scripts\python.exe" -B build_documents.py
```

Only PDF rebuilding needs reportlab/pypdf. Keep the environment outside the submission. The fresh-run log and resolved dependencies are in [evidence/cold-run.log](evidence/cold-run.log) and [evidence/cold-environment.txt](evidence/cold-environment.txt). The clean run executes analysis and HTTP checks before installing any third-party packages, then rebuilds the PDFs. PDF pages were rendered and inspected separately for layout.

## Model development and provenance

| Source version | Contribution |
| --- | --- |
| Edition A and September research | Unchanged baseline; thesis, normalized-earnings issue and evolution |
| Lab 6 | FCFF/WACC/terminal, grid and reverse-DCF methods, now using pro-forma cash flows |
| Lab 08 | Predeclared peer policy, primary-source exclusions and consistent multiple definitions |
| Lab 09 | Known-answer validation fixture, not a second DUOL model |
| Lab 10 | Core statement sequence, company-specific drivers, cash-last accounting and failure checks |
| Lab 11 | One-at-a-time EBIT/FCFF/value, reset and range dependence; original prediction history preserved |
| Lab 12 | Interpretation, monitoring and actual recorded partner challenges |

The compact code is `model.py` (one engine), `analysis.py` (required analyses/report), `panel.py` (bounded interface), `validate.py` (independent tests), and `build_documents.py` (PDF packaging). There is no duplicate active DUOL engine. The complete lab-to-requirements review is retained as [supporting evidence](evidence/lab-to-project-map.md); it describes the pre-consolidation gaps and plan, not the current completion status.

## Important corrections and limitations

Lab 10/11 originally gave $140.18. The final $137.57 adds filed H1 data, September stub timing, a dated liquidity bridge with an operating reserve, asset depreciation allocation, and terminal reinvestment at mature growth. The difference is a set of corrections, not a single-factor attribution. The final cash reconciliation increases the prior $136.89 estimate by $0.68 per share. Estimated dated cash now ties to the accounting cash-flow forecast, with repurchase settlement classified as financing. No target value is imposed.

Lab 11's current two named drivers both change revenue growth at different widths; a prose paragraph instead says gross margin. The original Git prediction used gross margin. Both records remain intact. The final model distinguishes growth, margin and SBC; equal growth shocks under different names produce identical outputs. Wider shocks can determine apparent sensitivity ranking.

The final model rejects the FCFF-only corruption that the original Lab 10 checks accepted. It enforces 148 accounting/input checks and passes 70 additional validation tests, including the Lab 09 $291.75 answer, source facts, grid directions, peer definitions and future-cash double counting. The 54 panel HTTP checks test bounds, invalid requests, failure and recovery. Check evidence is in outputs/ and evidence/; exact current counts/time are in outputs/run-status.json.

Terminal value is 84.34% of EV and its implied ROIC (about 101%) is demanding. Named downside stresses (outputs/named_stresses.csv) each change one disputed judgment: terminal ROIC 20% $126.01; no 2027 growth reacceleration $127.16; growth at the FY2026 bookings pace $122.63; beta 1.0 $125.56; total-return beta $134.15. The regression beta of 0.85 has an R-squared of 0.045 (outputs/wacc.json). All stresses lower value; none reverses Watch / Defer. Estimated September liquidity is not an observed filed balance. Peer exclusions leave no defensible independent peer target: own-company EV/earnings ratios are consistency checks, not peer corroboration. Guidance, historical ratios and judgments are labeled; all 24 drivers have challenges and revision evidence.

## Required demo - first minute of Video 3

Move growth or gross margin and explain the changed statements/value. Select one-driver sensitivity to see low/base/high with others held at base. Reset restores all inputs. The failure button sends terminal growth equal to WACC to the actual DCF on a copy; the displayed valuation clears and an error appears. Reset recovers. This sequence supports the live opening of Video 3.

Demo checklist (an operating guide, not a transcript):

1. Launch `python -B panel.py` and open http://127.0.0.1:8765. Keep the terminal running.
2. Show the dated Watch / Defer decision, confirmed 3-5-year horizon and fixed operating-scenario range.
3. Move gross margin by +1 percentage point. Trace gross profit to EBIT, after-tax FCFF and value; the saved base is $137.57 and this example is approximately $142.86. This disclosed rehearsal is not a new AI-off prediction test.
4. Reset to base and explain the one-driver sensitivity table. Other assumptions are held at their original base in that table.
5. Click the deliberate terminal-growth failure. Show the error and cleared live results, then reset and recover.
6. Continue the committee defense with the tool on screen. Explain the dated market price, terminal-value risk and monitoring conditions with reference to the model.

No hosted frontend, extra website or slide deck is needed. This browser panel is the frontend.

## Submission status

The model, executed output, research evolution, decision memo and validation record are complete. AI use (Codex gpt-6-astra; Claude Opus 5.5 review) is disclosed in the validation record.

The remaining submission items are:

1. Edition A checkpoint/receipt resolution with the instructor through the course process.
2. Video 1 (research evolution, maximum 3 minutes), Video 2 (code/validation, maximum 5 minutes), and Video 3 (live demonstration and committee defense, maximum 5 minutes).
3. Three corrected transcripts derived from the actual recordings.
4. Recording links, durations, timestamp indexes, frozen version and access checks in the manifest.
5. Repository publication, Brightspace submission and retained receipt.

The Locked Changed-Input Record includes my in-class AI-closed prediction and reproduced historical results. Exact historical execution timing and a contemporaneous formal action statement are not separately established.

Official references: [Project 1](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/projects/project-1-corporate-finance-application.md), [shared checklist](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/projects/major-project-student-checklist.md), [AI boundary](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/projects/AI-BOUNDARY-CARD.md). Brightspace controls dates and individual recovery arrangements.

Known repository: https://github.com/Mrigna01/DUOL-research . Publication of this local final folder and grader access are unverified. No upload or commit is claimed. The SHA256 file list in evidence/package-hashes.json identifies this local review snapshot; update it after any final edits.
