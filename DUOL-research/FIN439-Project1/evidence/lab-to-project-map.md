# Lab-to-Project 1 map and minimum final scope

## Conclusion

The labs are the foundation of this project. The course does not require a folder named duol_valuation, an additional valuation assignment, a 17-module package, or two competing models. The existing labs are not yet a complete final bundle, however. Reuse their analysis and add only the missing final requirements. The previously assembled FIN439-Project1 package is an alternative implementation, not proof that its entire contents are mandatory.

This review inspected the original research, Lab 6, Lab 08 and its evidence, Lab 09, Lab 10, Lab 11 and its Git history, and Lab 12. Original paths below are relative to the parent DUOL-research repository. Original files were not edited. Python modules were imported with bytecode disabled and functions called without their file-writing main routines.

Official specification: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/projects/project-1-corporate-finance-application.md
Shared checklist: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/projects/major-project-student-checklist.md

## Original file disposition

| Original file/group | Contribution | Final treatment |
| --- | --- | --- |
| Duolingo_2026-09-01_edition-a-draft.md | Original thesis, assumptions, evidence, unknowns | REQUIRED baseline: preserve unchanged; reproduce in Research Evolution. Receipt remains a separate requirement. |
| DUOL-10-K.pdf | Primary historical financial evidence | SUPPORTING EVIDENCE: retain one copy, with precise statement locators. |
| Duolingo_2026-09-03_report.md | Business thesis, tax normalization concern, watch/defer reasoning | MERGE supported analysis into Edition B; do not submit as another final recommendation. Omit unresolved claims from final prose. |
| sources.md | Historical source map | MERGE verified locators; repair obsolete missing DCF link in the final source record, not in historical original. |
| Lab 6.md; dcf.py | FCFF/WACC/terminal/bridge concepts, sensitivity grid, reverse DCF and known-answer fixture | MERGE methods into the selected pro-forma-driven engine. Preserve $251.99 as historical research evolution only, not current target. |
| lab08.md | Predeclared peer policy, exclusions, corporate action, methods disagreement and source checks | MERGE policy and sourced limitations into final records. Do not manufacture peer estimates. |
| lab08_comps.py | P/E calculator with empty admitted peer set | SUPPORTING EVIDENCE; no need for a second active final valuation engine. Own-company EV and equity multiples still need explicit calculations. |
| lab08_evidence/policy-and-prerun-prediction.md | Earlier policy and prediction record | SUPPORTING EVIDENCE; retain attribution (agent-authored is disclosed in lab). |
| lab08_evidence/source-verification.md; README.md | Source and evidence definitions | MERGE relevant locators into final source/validation record. |
| lab08_evidence/calculator-output.txt; validation-output.txt | Actual calculator and definition outcomes | SUPPORTING EVIDENCE; retain relevant excerpts or files. |
| lab08_evidence/nasdaq-cour-final.json; nasdaq-duol-final.json | September 10 price corroboration | SUPPORTING EVIDENCE for historical lab comparison; do not label September 21 prices. |
| lab08_evidence/lab07-baseline-output.txt | Training-case comparator baseline | OPTIONAL if Lab 09 supplies the required known-answer evidence; not another DUOL result. |
| lab08_evidence/week03-dcf-rerun.txt | Earlier $251.99 DCF reproduction | SUPPORTING evolution evidence; avoid duplicating its entire output in the final model. |
| lab09/proforma.py; lab09/lab09.md | ABG known-answer engine and broken-cash check | SUPPORTING validation fixture. ABG FCFE is not the DUOL FCFF engine. |
| lab10/duol_proforma.py; lab10/lab10.md | DUOL five-year operating model and assumption explanations | CORE REUSE: best small lab-based starting point; close the accounting/display/timing gaps below before final use. |
| lab11/lab11_sensitivity.py; sensitivity_results.csv; lab11.md | OAT EBIT/FCFF/value, restore-base, range interpretation and partner challenges | MERGE into a single model implementation; do not keep the copied Lab 10 engine as a second active engine. |
| lab11/locked_changed_input_record.md | Existing prediction, results and Git history | SUPPORTING EVIDENCE requiring reconciliation, not missing. Preserve historical versions; do not rewrite the original precommit. |
| lab12/lab12.md | Presentation narrative, conditional interpretation, monitoring and partner exchange | CORE writing source for Edition B and memo; exclude unrelated Apple discussion except concise review attribution if relevant. |
| duol_valuation/; duol_valuation_submission.zip | Separate expanded implementation and outputs | NOT REQUIRED AS A WHOLE. Reuse selected source evidence or missing functions only where useful; do not submit both alongside a duplicated lab-based engine. |
| FIN439-Project1/duol_valuation/ | Previously prepared alternative, with validated additional functions | REFERENCE during consolidation. It is not a mandated directory. Existing $136.89 PDFs are tied to this engine and cannot be paired with $140.18 lab outputs unchanged. |

## Requirement-by-requirement comparison

?Present? means evidence exists in the labs, not that every claim has been certified. ?Partial? means substantive reuse is possible but final reconciliation is needed.

| Project 1 requirement | Lab evidence | Status and minimum work |
| --- | --- | --- |
| Unchanged Edition A | Original Edition A file | Present; preserve. Brightspace receipt/recovery remains unresolved evidence. |
| Edition B / research evolution | September report and Labs 6, 08, 10?12 | Partial; merge into one dated narrative and A-to-B table. |
| Five-year three-statement pro forma | Lab 10 operating and balance-sheet engine | Partial; display full assets/liabilities and CFO/CFI/CFF/cash reconciliation, not just FCFF and cash. |
| Normalized base year / contamination catalog | September report tax discussion; Labs 6, 08, 10 | Partial; one explicit numerical bridge and contamination catalog; distinguish reported FCF from operating FCFF. |
| Company-specific driver architecture | Labs 10?12 subscriber, deferred revenue, AI, SBC and cost reasoning | Present foundation; connect each driver to values, evidence and limitations. No invented standalone AI revenue series. |
| FCFF DCF | Lab 10 | Present; strengthen identity checks and date convention. |
| WACC | Lab 6 derivation; Lab 10 hard-coded updated rate | Partial; reconcile old 8.5286% with later 8.2764%, retain dated inputs and beta method. |
| Terminal value | Labs 6 and 10 | Present; review terminal working-capital reinvestment instead of assuming last-year FCFF growth is automatically sustainable. |
| Enterprise-to-equity bridge | Lab 10 opening cash and investments | Partial; date liquidity consistently, define operating reserve, shares and debt; avoid adding future cash. |
| Low/base/high causal scenarios | Lab 11 OAT cases | Partial; OAT tests are not automatically integrated causal operating scenarios. Add three coherent cases on the same engine. |
| WACC ? terminal-growth sensitivity | Lab 6 | Partial; rerun on final Lab 10-derived FCFF, not old starting FCF. |
| Terminal-value share | Labs 6 and 10 | Present; report final engine result and interpretation. |
| Reverse DCF / market-implied expectation | Lab 6 solver | Partial; solve against final pro-forma engine and matching price date. |
| Comparable-company policy | Lab 08 and dated evidence | Present; retain exclusions and process attribution. |
| At least one EV multiple | Not established by the lab P/E calculator | Gap; calculate a consistently dated EV/sales or EV/EBITDA with explicit numerator bridge. |
| At least one equity-value multiple | Lab 08 EPS and price, no admitted peer estimate | Partial; explicitly compute DUOL price/EPS or equity/earnings and qualify tax contamination. |
| Disagreement across methods | Lab 08 and September report | Present foundation; update with final normalization and DCF, no mechanical average. |
| Assumption-challenge record | Lab 10 assumptions and Labs 10?12 exchanges | Partial; every material driver needs a challenge and revision evidence; credit actual reviewers where identifiable. |
| Pro-forma articulation checks | Lab 10 balance and cash-floor tests | Partial; add cash roll-forward, FCFF identity and opening filing reconciliation. |
| DCF monotonicity checks | Lab 6 grid displays direction | Partial; assert expected directions on final engine and reject incoherent inputs. |
| Enterprise-equity bridge checks | Lab formulas | Partial; independent reconstruction and double-count test needed. |
| Peer/multiple consistency check | Lab 08 exclusions and source verification | Present foundation; extend to final EV and equity definitions/date. |
| Known-answer / synthetic reconciliation | Lab 09 and Lab 6 training case | Present; Lab 09 reproduced $291.75166628 in this audit. Retain one primary fixture. |
| Independent source/definition check | Lab 08 source verification; Lab 10 filing checks | Present foundation; link a load-bearing final input and its actual independent evidence. |
| Directional changed-input test | Lab 11 predictions and output | Present, with AI-channel mismatch that requires reconciliation. |
| Locked Changed-Input Record | lab11/locked_changed_input_record.md and Git | Partial, NOT absent. Verify AI-off authorship and sequence, reconcile changed input definition, and add committee-action effect/no-change explanation. |
| Highest-risk failure test | Lab 10 deliberate cash corruption | Partial; useful test, but FCFF-only corruption currently escapes. Add that test and bridge double counting. |
| Cold run | Individual run instructions, no integrated final cold log | Gap for a newly consolidated engine; rerun clean after consolidation. Prior alternative-package cold run cannot certify new code. |
| Independently validated AI output | Lab 08 disclosure/source checks | Partial; name a particular AI output, evidence and accept/modify/reject disposition; student review required. |
| Visible executed output | Lab writeups and Lab 11 CSV | Present foundation; regenerate a single consistent final output. |
| Semi-adjustable bounded workbench | No interactive panel in original labs | Gap; one small panel over the selected engine is required. Hosting and a large application are not. |
| Reset-to-base behavior | Lab 11 resets in code | Partial; expose reset in the panel and verify visible results. |
| Fail-loudly checks | Lab 10 raises on broken cash | Partial; surface errors and clear stale output in the panel. |
| Final valuation range | Labs 6 and 11 ranges | Partial; choose one final causal range and distinguish OAT/grid stresses from probabilities. |
| Initiate / Watch-Defer / Do Not Initiate | Lab 6 conditional initiate; Lab 08 watch; Lab 12 reasonably valued | Partial; reconcile one final committee action with dated evidence. Do not silently overwrite evolution. |
| Monitoring / reversal triggers | September report and Lab 12 | Present foundation; tie final conditions to the chosen operating thesis and decision. |
| README with run instructions | Per-lab commands | Gap for one final integrated package; create one short root README. |
| Research-evolution PDF | No original final PDF | Final packaging requirement; reuse existing lab narrative. |
| Decision memo/deck | Lab 12 narrative | Final packaging requirement; a two-page memo is enough, no additional deck required. |
| Validation-and-AI-use record | Evidence scattered across labs | Partial; consolidate, with accurate unresolved human evidence. |
| Three corrected transcripts | No actual transcript files found | Missing; derive from actual student recordings, not lab prose. |
| Three required videos | No actual recordings found in repository | Missing locally; use existing external recordings if available and verify links. |
| Frozen manifest and access checks | Not established by labs | Final handoff requirement; fill only actual locations, version and access results. |

## Conflicts that must not be merged silently

1. **Valuation lineage:** Lab 6 gives $251.99 using reported-FCF starting input, September 10 price, 48.308m shares and 8.5286% WACC. Labs 10?12 use a $140.18 pro-forma result, September 21 price, 50.7m shares and 8.2764% WACC. The separate expanded model gives $136.89 with further timing/bridge/terminal conventions. These are different versions, not three estimates to average.
2. **AI driver:** current Lab 11 code and result tables shock revenue growth by ?1pp; its partner-exchange paragraph still says gross margin. The two current named drivers change the same model parameter at different widths. They represent alternative stories for growth, not separately estimated independent economic factors. At equal growth shocks their outputs must be identical.
3. **Prediction history:** Git commit 3c6dab3 (September 29, 2026, 17:28:03 ?0400) contains a prediction-only record whose AI driver is gross margin. Later commits e3aefff and f9d2c2e add results and change the AI input to revenue growth. This is useful preserved history. It does not by itself prove AI-off authorship or that the later revenue-growth prediction was locked before its run. Preserve the original and document the change; assess whether the original gross-margin experiment can satisfy the course rule before requiring a new test.
4. **Incomplete protection:** a read-only in-memory audit added $100m to 2026 FCFF alone. Lab 10 still returned $142.00483941 instead of rejecting the inconsistent FCFF. Its existing balance-sheet checks are useful but do not validate the FCFF identity.
5. **Timing and liquidity:** Lab 10 uses FY2025 opening cash and discounts all of 2026 as a future year while labeling the price September 21, 2026. It also adds the full cash balance while imposing a $100m operational cash floor. Resolve and disclose these conventions; do not change the date label merely to conceal the mismatch.
6. **WACC lineage:** the updated Lab 10 rate is a constant, not a reproducible derivation within that standalone script. The final source evidence must show how the selected rate was obtained.
7. **Historical research labels:** sources.md still links a nonexistent September 8 DCF file. Keep historical originals unchanged, but use valid links in the final source map.

## Smallest clean final structure

This is a target structure, not another newly created implementation:

```
FIN439-Project1/
  README.md
  requirements.txt                  # only packages actually used
  submission-manifest.csv
  model.py                          # one Lab 10-derived engine + Lab 6 DCF utilities
  analysis.py                       # Lab 11 scenarios, sensitivities, multiples and visible output
  panel.py                          # small bounded interface over model.py
  validate.py                       # final checks + Lab 09 known-answer fixture
  docs/
    edition-a.md                    # unchanged source
    research-evolution.md / Research-Evolution.pdf
    decision-memo.md / Decision-Memo.pdf
    validation-and-ai-use.md / Validation-and-AI-Use.pdf
    assumption-challenges.csv
    contamination-catalog.csv
    locked-changed-input-record.md  # actual preserved evidence + dated reconciliation
    transcript-video-1.txt          # only after actual recording/correction
    transcript-video-2.txt
    transcript-video-3.txt
  data/                            # one copy of necessary primary evidence + source ledger
  outputs/                         # final statements, valuation, sensitivities and visible report
  evidence/                        # selected lab evidence, test outputs and fresh cold-run log
```

The precise filenames are discretionary except the course's deliverable filenames. A single notebook with a driver panel can replace model.py/analysis.py/panel.py if it is genuinely simpler. Do not keep both architectures. Videos may be accessible links instead of large local files. A deck, hosted website, ZIP, duplicate SVG charts, extra valuation engines and unrelated peer-company research are unnecessary.

## Exact consolidation order

1. Preserve Edition A and original labs; select Lab 10 as the small canonical starting engine, Lab 11 for sensitivity behavior, Lab 6 for DCF utilities and Lab 09 for the known-answer fixture.
2. Close Lab 10's statement display, FCFF identity, valuation-date/cash bridge, WACC provenance and terminal-reinvestment gaps. Reuse relevant functions/evidence from the expanded implementation only when they solve one of these requirements. Do not maintain both engines.
3. Resolve the AI driver inconsistency and preserve the historical locked record. Keep growth and AI-cost effects distinct when testing distinct economic mechanisms; explicitly test shock-width dependence.
4. Add only missing final calculations: normalized bridge/catalog, causal scenarios, final-engine grid/reverse DCF, consistent EV/equity multiples and independent checks.
5. Put one bounded panel on that engine and retain a visible, executed report. Run the final checks and a new clean end-to-end reproduction.
6. Rewrite the existing final document drafts around that selected output, using Lab 12 and the historical evolution. The old $136.89 drafts must not be represented as conclusions of the $140.18 lab engine without reconciliation.
7. Verify whether the existing student prediction evidence qualifies. Obtain genuinely missing student evidence, recordings, corrected transcripts, access checks and receipt; do not fabricate or retrospectively relabel it.
8. Freeze and submit only the consolidated package. Leave the original duol_valuation folder and ZIP as historical/optional material outside the submission, unless specific evidence was deliberately selected.

This review completes the mapping and scope decision. It does not claim the lab-based consolidated engine has already been built or its future results validated. No original lab code or historical prediction was modified.
