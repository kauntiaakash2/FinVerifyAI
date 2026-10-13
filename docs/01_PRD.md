# Product Requirements Document (PRD)
Version 0.1 | Draft, not user-validated.

## 1. Problem
Numeric statements about a public company's financial performance are easily misread when fiscal periods, filing contexts, restatements, accounting concepts, currencies and scales differ. A current quote/summary field cannot reliably validate a historical claim.

## 2. Primary personas and jobs
- Equity research assistant: inspect claims against primary SEC filings; export defensible references.
- Financial journalist/fact-checker: resolve reported figure and fiscal period with source link.
- Finance student/researcher: learn why a claim is supported, contradicted, ambiguous or unverifiable.
Pilot only after interviewing >=5 relevant users and obtaining examples of their real workflow.

## 3. Proposed positioning
"Verify factual numerical claims about US public-company filings with reproducible source evidence and explicit uncertainty." This is not trading advice, investment recommendations, fraud detection or audit certification.

## 4. Scope MVP
- User enters a single English-language claim; optional ticker/period hints.
- Support 10 selected US SEC-reporting issuers, fiscal annual revenue and selected net income / EPS concepts only after mapping validated. Explicit coverage registry.
- Extract: company identity (prefer CIK), filing context, metric taxonomy, amount, unit, currency, annual/quarter/TTM, fiscal period, qualifiers, filing as-of date.
- Retrieve SEC submissions and XBRL/companyfacts, original filing URLs and accession metadata; cache with provenance.
- Deterministic normalization/comparison with configurable documented rounding tolerances.
- Return SUPPORTED / CONTRADICTED / INSUFFICIENT_EVIDENCE / AMBIGUOUS / OUT_OF_SCOPE, plus typed error states where applicable.
- Show evidence trail, extracted facts, relevant filing metadata, comparison rationale, and limitations.
- Provide accessible responsive UI and documented public API with resource limits.
- Benchmark against a frozen labeled dataset. Release report with precision, recall, coverage, abstention and error breakdown.

## 5. Non-goals MVP
- International accounting frameworks, cryptocurrency and non-public companies.
- Intraday share prices, share-price predictions, trading signals, investment advice.
- All financial concepts, all fiscal adjustments, claims without a numeric core, guaranteed truth, or autonomous financial decisions.
- PDF uploads and batch document processing before single-claim accuracy is verified.

## 6. User stories and acceptance criteria
FR-01: As a researcher, I can submit a claim and receive typed extracted entities or an explicit extraction failure; original string preserved.
FR-02: As an analyst, I can see the actual fiscal period and taxonomy concept used, or an explicit ambiguity explanation.
FR-03: As a reviewer, I can access a source citation resolving to the relevant SEC filing/structured fact and distinguish retrieved_at from filed_at and period_end.
FR-04: As a journalist, I can see normalized amount/currency/scale and rounding rationale; no financial value is silently inferred.
FR-05: As a user, unavailable evidence never becomes CONTRADICTED or a zero-value fact.
FR-06: As an API consumer, I receive machine-readable result status and stable structured errors; upstream failures do not falsely return success.
FR-07: As an operator, I can view traceable errors, request limits, dependency health, and versioned evaluation artifacts.
FR-08: As a keyboard/screen-reader user, the input, status and evidence are fully operable and announced.
FR-09: As a reviewer, the system does not claim a probability of correctness without calibration evidence.

## 7. Non-functional targets (provisional, revise after baseline)
- Zero known critical/high exploitable security issues at release; defined abuse budgets.
- 100% passing deterministic unit tests, contract tests, and golden fixtures on release branch.
- No false support on curated 'wrong period/wrong company/wrong unit' adversarial cases.
- Dataset-level success thresholds defined in 07_AI_AND_EVALUATION before experiments; no post-hoc threshold cherry-picking.
- p95 latency and cost budgets measured and approved after a real dataset and hosting tier are chosen.

## 8. Business assumptions to test
Willingness to use/return, perceived advantage over SEC search and existing tools, acceptable verification latency, frequency of claims, and importance of audit trail. No evidence of paying customers or product-market fit yet.

## 9. Success and kill criteria
Pilot success: >=5 realistic user tasks, credible time-saving/accuracy evidence, and >=1 user willing to retest. Kill/pivot: can't distinguish periods reliably, lack lawful dependable evidence access, or pilot users prefer existing workflows with no measurable improvement.
