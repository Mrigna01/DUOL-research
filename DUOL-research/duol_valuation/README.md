# Duolingo pro-forma valuation — FIN 43900 Weeks 5–6

Open **duol_valuation.ipynb** first (or outputs/duol_valuation.html for a rendered copy). This project reproduces the FIN439 ABG workflow for NASDAQ: DUOL: sourced history, labelled assumptions, one linked forecast year, mandatory checks, deliberate failures, five years, regression beta, WACC, FCFF valuation, seven rates, shocks, named cases and market-implied conditions.

Historical years: 2023–2025. Forecast: 2026–2030; 2026 combines reported H1 with forecast H2. Valuation date: September 21, 2026 close. Raw snapshots make reruns independent of network availability. Original parent-folder work remains unchanged.

Python 3.11+ required; developed and executed on Python 3.13.9. From DUOL-research:

```powershell
python -m pip install -r duol_valuation/requirements.txt
python duol_valuation/run.py
```

The second command runs the model, controlled failure tests, sensitivity and root searches, independent audit, charts, notebook execution, HTML export and local panel HTTP smoke test. An exception stops the build if a required check fails. To use the panel:

```powershell
python duol_valuation/panel.py
```

It serves only on 127.0.0.1:8765; open that address. Growth, gross margin and WACC controls rerun the same model and show check results. Stop with Ctrl+C.

## Files

- `duol_valuation.ipynb`: executed primary deliverable, all 25 requested sections.
- `valuation_summary.md`: detailed auditable valuation, bridge and limitations.
- `presentation_brief.md`: colleague briefing, eight numerical answers, triggers, predictions and simulated sceptic discussion.
- `assumptions.csv`: year-specific inputs and source categories, plus parameter shock values.
- `model_conventions.csv`: additional modelling boundaries and allocation choices, all labelled.
- `model_checks.csv`: all mandatory forecast and historical checks.
- `src/`: readable model modules; `run.py`: full reproducible build.
- `data/raw/`: SEC companyfacts, course slides/captions, interim shareholder letter, dated market data, Damodaran input snapshot, inventory and source/retrieval notes.
- `data/processed/`: extracted financial statements, prices and cell-level source ledger.
- `outputs/tables/`: model results, scenarios, audit, ABG comparison, failure tests, panel verification and source integrity hashes.
- `outputs/figures/`: seven model-derived charts, PNG and SVG.
- `outputs/duol_valuation.html`: static notebook view with figures and outputs.

## Method and controls

The professor values ABG equity directly using FCFE; DUOL is valued using FCFF and WACC because it has no traditional debt. Operating leases remain operating throughout. SBC is expensed in EBIT and not added back in FCFF. Accounting cash flow adds back SBC and credits equity. Cash is the end result of operating, investing and financing flows. Full statement and roll-forward checks are recalculated inside every DCF call; changing a cached total cannot bypass them.

The model uses 61 monthly DUOL/SPY closes, August 2021–August 2026, producing 60 monthly returns. Adjusted-price and Blume alternatives are reported. Treasury and ERP are explicitly dated September 1; do not describe them as September 21 quotes. The date bridge, diluted-share convention, frozen deferred tax assets and terminal reinvestment limitations are described in `LIMITATIONS.md`.

## Sources and reuse

Existing `../DUOL-10-K.pdf` was inventoried; its corresponding `../lab08_evidence/duol-2025-10k.html` and existing extracted PDF evidence were inspected/reused. No raw parent source was overwritten. SEC companyfacts stores exact facts with accession/date locators. Historical statement values were cross-checked to the filing. The Q2 2026 letter supplies guidance and dilution; the 10-Q supplies H1 financials. Yahoo monthly prices are frozen, and Nasdaq independently confirms the September 21 close. Source URLs and download status are in data/raw and the summary.

## Submission

Course Labs 11–12 specify **GitHub links to markdown, Python and supporting files**, not a single mandated notebook format. The complete `duol_valuation/` folder is the submission bundle: include the executed notebook, markdown briefs, assumptions/checks/conventions, source code, requirements, frozen data and outputs. A local submission ZIP is built next to the folder. No upload is performed. Human partner discussion and oral assessment remain human course activities; simulated questions are clearly labelled and must not be presented as completed peer review.

Learning exercise, not investment research or financial advice.
