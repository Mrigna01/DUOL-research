# Lab 08 submission files

The main submission is [lab08.md](../lab08.md), supported by the single assignment calculator [lab08_comps.py](../lab08_comps.py).

## Included evidence

- `policy-and-prerun-prediction.md`: initial policy and prediction checkpoint.
- `nasdaq-duol-final.json`, `nasdaq-cour-final.json`: verified September 10, 2026 closing-price rows; preserve the financial input evidence.
- `calculator-output.txt`, `validation-output.txt`: actual program outputs.
- `week03-dcf-rerun.txt`: saved DCF reproduced without changing its inputs.
- `lab07-baseline-output.txt`: original Lab 07 case, explicitly retained only as a regression baseline.
- `source-verification.md`: source inspection notes; canonical URLs and locators are in the report.

Existing `dcf.py`, `Lab 6.md`, `DUOL-10-K.pdf` and the repository-root Lab 07 calculator are reused without modification. Duplicate source downloads, course-page snapshots, failed API responses, raw retrieval logs and Python caches are not part of this submission.

## Run

From the repository's `DUOL-research` directory:

```powershell
python .\lab08_comps.py
```

Expected result: no admissible peer estimate. Independent checks were completed locally; their output is retained as evidence. The optional validation script is not part of the submission. No third-party packages are required.

## Remaining checkout

Review and own the analysis, complete the disclosed personal partner/independent-AI requirements, and submit the GitHub links to Brightspace when instructed. No Brightspace submission was performed.

UNRESOLVED: the saved DCF's exact historical Treasury quote and beta snapshot. The dated ERP is corroborated. See report section 12 for the Treasury observation difference and its treatment. Both peer exclusions are evidenced decisions, not unresolved data blanks.
