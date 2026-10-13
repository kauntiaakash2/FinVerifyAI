# Domain Data Model & API Contract
Status: draft contract subject to ADR review.

## Entities
Issuer(id, cik UNIQUE, legal_name, aliases[], symbol_history[])
Claim(id, raw_text, submitted_at, user_id nullable, scope_version, extraction_version)
ParsedFact(claim_id, issuer_id?, concept?, amount Decimal?, unit?, currency?, period_type?, fiscal_year?, fiscal_quarter?, period_start?, period_end?, qualifiers?, extraction_state)
Evidence(id, provider, accession, filing_type, document_url, filed_at, period_start, period_end, taxonomy, concept, unit, value Decimal, fetched_at, content_hash)
Verification(id, claim_id, verdict enum, reason_codes[], evidence_ids[], algorithm_version, comparison_policy_version, evaluated_at)
AuditEvent(id, actor, event, target_id, at, request_id, redacted_metadata)
Avoid float for currency and exact decimal comparisons.

## API endpoints
POST /api/v1/verifications: accepts {claim, issuer_hint?, as_of_date?}; returns typed verdict and evidence identifiers; 202 only for asynchronous jobs.
GET /api/v1/verifications/{id}: persistent result where feature enabled; scoped authorization.
GET /api/v1/coverage: supported jurisdictions/issuers/concepts/periods.
GET /api/v1/health/live and /api/v1/health/ready: process and dependency readiness separately.
GET /api/v1/openapi.json: versioned API schema.

## Response outline
```json
{
 "verification_id":"uuid",
 "verdict":"SUPPORTED",
 "reason_codes":["FISCAL_PERIOD_MATCH","ROUNDING_MATCH"],
 "parsed_claim":{"issuer_cik":"0000320193","metric":"us-gaap:Revenues","period_type":"FY","fiscal_year":2023,"amount":"383300000000","currency":"USD"},
 "evidence":[{"provider":"SEC_EDGAR","filing_accession":"example-only","filed_at":"YYYY-MM-DD","period_end":"YYYY-MM-DD","document_url":"https://www.sec.gov/...","fact_amount":"383285000000","unit":"USD"}],
 "comparison":{"difference":"15000000","tolerance_basis":"ROUNDING_TO_0.1_BILLION"},
 "versions":{"verification_policy":"v1","extractor":"baseline-v1"},
 "evaluated_at":"ISO-8601"
}
```
Example shape only; accession and document URL placeholders are not actual sources.

## Errors
Use 400 malformed request, 413 size, 422 validation, 429 rate limit, 503 evidence provider unavailable (or a successful typed INSUFFICIENT_EVIDENCE only when processing completed and reason is nonfatal), 500 internal errors without stack traces. Correlation ID everywhere. Define idempotency semantics for writes and retry-safe operations.

## Privacy
No personal investor holdings; avoid mandatory accounts in MVP. Opt-in stored history; anonymized telemetry only; authenticated export/deletion once history exists.
