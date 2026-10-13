# Financial Claim Semantics and Verification Contract
This is the product's highest-priority correctness specification.

## Canonical claim tuple
{issuer_cik, issuer_name, metric_concept, amount_decimal, currency, scale, financial_period_type, fiscal_year, fiscal_quarter, period_start, period_end, filing_as_of, accounting_basis, consolidated_scope, comparison_operator, qualifiers, extraction_provenance}
Missing or conflicting critical values => AMBIGUOUS / INSUFFICIENT_EVIDENCE, not invented.

## Evidence fact tuple
{source_provider, filing_accession, document_url, filing_type, filed_at, period_start, period_end, fiscal_year, fiscal_quarter, frame, taxonomy_name, taxonomy_concept, unit, value_decimal, context_identifiers, amendments_or_restated_flag, fetched_at, evidence_excerpt_or_location, checksum}
Keep filing time and retrieval time separate.

## Matching rules
1. Resolve unique issuer by CIK; ticker is a mutable alias, not primary identity.
2. Normalize metric with an explicit governed concept map; 'earnings' alone is ambiguous.
3. Map fiscal year/quarter and interval vs instant (revenue is duration; assets instant). Do not use calendar quarters by default.
4. Disambiguate standalone quarter from year-to-date, full fiscal year, or trailing twelve months; never subtract YTD without explicit validated logic.
5. Match USD/other currencies and scale; no implicit FX conversion. Require currency and period for cross-currency comparisons.
6. Handle values expressed as percentage points, ratios or percentages; e.g. 0.20 -> 20% only when concept/unit implies ratio. Do not interchange share-price growth with revenue growth.
7. Consider original vs amended/restated filings and an explicit user-chosen as-of policy; record policy on each verdict.
8. Match qualifiers ('about', 'more than', 'at least'), and rounding based on stated precision. Define threshold as numeric rounding interval rather than arbitrary 'confidence'.
9. If no exact context match, abstain with explanation. Null, 0, failure, unsupported metric, and truly reported zero are distinct.
10. Derived metrics require separately evidenced numerator/denominator, formulas and alignment.

## Verdicts
SUPPORTED = evidence aligns with all critical dimensions and claim meets comparison/tolerance.
CONTRADICTED = complete, correctly matched evidence explicitly conflicts with the claim.
AMBIGUOUS = competing interpretations or missing critical claim dimension.
INSUFFICIENT_EVIDENCE = source unavailable, missing fact, incompatible context, or provider failure after retries (with typed status).
OUT_OF_SCOPE = unsupported issuer/metric/jurisdiction/type.
Do NOT display an uncalibrated percentage 'confidence'. Display evidence quality dimensions: source type, period matching, extraction ambiguity and recency.

## Adversarial fixtures (minimum)
Correct historical annual claim vs current revenue; FY vs calendar year; quarter vs YTD; ratio 0.2 vs 20%; stock vs revenue growth; currency mismatch; ticker collision; negative net income; zero reported figure; delayed filing; multiple filings/restatements; rounding; malformed claim; compound claims; source 429/timeout; missing XBRL concept. Ensure each expected outcome is fixed before implementation.
