# AI Design, Benchmarking & Evaluation Protocol
Status: methodology specified; benchmarks not yet run.

## Principle
Use AI for extraction/retrieval assistance where it measurably outperforms baselines; use deterministic Decimal arithmetic for verdicts. Never let model output alone determine 'supported'.

## Baselines
B0 existing regex + current yfinance comparator (label as inadequate for temporal verification); B1 improved regex/entity resolver + SEC structured context; B2 optional LLM structured extractor with schema validator and explicit abstention. Do not compare on unequal information access.

## Dataset specification
Minimum pilot: 200 independently labeled claims spanning >=10 issuers, 3+ fiscal years if available, metric/period/unit diversity. Include 40+ explicitly adversarial or abstention claims. Expand to >=500 after pilot. Avoid assuming historical figures remain unrevised. Obtain immutable filing snapshots/accession refs and licensing provenance.

## Labels and splits
Claims have gold {issuer CIK, concept, amount, currency, period, filing and verdict}. Annotate by two reviewers on a subset; adjudicate disagreement. Split by issuer and reporting periods where feasible; publish leakage analysis. Freeze test labels before tuning.

## Metrics
Extraction: exact-match entity/metric/period and normalized amount correctness; confusion breakdown.
Retrieval: evidence recall@k and citation validity.
Verifier: macro-F1 per verdict, precision on SUPPORTED, false-SUPPORTED count/rate, abstention calibration, supported coverage conditional on sufficient evidence.
Systems: p50/p95 latency, request cost, upstream errors, token usage, repeatability; stratify by metric, year, issuer and claim style.

## Precommitted gates (proposals, validate feasibility)
- >=95% precision for SUPPORTED on untouched in-scope test set; zero false-supported on designated critical temporal/unit fixtures.
- >=90% exact period alignment on clearly stated period claims.
- 100% programmatically validated source URL provenance for SUPPORTED outcomes.
- Publish actual recall/abstention; never silently optimize precision through rejecting every claim.
- No exposed test label tuning or unsupported accuracy claim in README.

## Optional model risks
Prompt injection from filings, structured-output validity, provider outage, privacy of submitted text, calibration and model version drift. Require offline baseline and failure path if LLM unavailable.

## Reproducibility
Record dataset version, model/prompt versions, dependencies, seed where relevant, evaluations as CI artifacts, confusion matrices, error exemplars, and links to labeled fixtures (subject to licensing).
