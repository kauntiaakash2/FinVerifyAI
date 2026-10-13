# Security, Privacy & Threat Model
Status: design controls; must be validated through tests before release. Target OWASP ASVS 5.0.0 L2-aligned controls as appropriate to scope; no compliance certification claim.

## Assets and attackers
Assets: API keys, user-submitted text/documents, stored claim history, financial evidence integrity, deployment credentials, service availability. Threat actors: abusive anonymous clients, malicious uploaders, upstream content injecting instructions, compromised dependencies, unauthorized authenticated users, deployment token leakage.

## Threat scenarios / mitigations
- API abuse and scraping -> shared distributed rate limits, quotas, max body sizes, timeouts, WAF, bounded batch size, no trust in forwarded IP headers except configured proxies.
- Cross-user result leakage -> object-level authorization, tenant-scoped queries, negative tests; avoid persistent user data in MVP.
- Stored/reflected XSS -> textContent/escaping, CSP, sanitization of any rich text, no innerHTML with external strings.
- SSRF -> hardcoded allowlisted SEC domains; block redirects to unapproved hosts; never accept arbitrary download URLs.
- File upload exploitation (later) -> size/type validation, signature sniffing, antivirus scanning as applicable, isolation, no direct execution, retention/deletion.
- Prompt injection -> filing content is untrusted; LLM may extract only schema-bound facts; never grant tools/credentials or let model decide numeric truth.
- Hallucinated citations -> server validates canonical SEC URL and fact linkage; no unverifiable evidence = no supported verdict.
- Dependency compromises -> pin/lock versions, automated SCA, SBOM, secret scanning, protected branches and review.
- Data source tampering/staleness -> provenance metadata, checksums, source freshness rules, restatement policy, signed deployment artifacts where feasible.
- Availability -> upstream retries with exponential backoff, deadlines, circuit breaker, capped concurrency and cache.
- Error disclosure -> stable public error codes, no tracebacks/secrets in responses, restricted logs and dashboards.

## Required controls and tests
HTTPS, HSTS as applicable, secure cookies if auth, restrictive CORS origins, CSRF defense for cookie-based state mutations, secure response headers, secrets manager, rotation playbook, structured audit events, least-privilege IAM, security regression tests, dependency scan, secret scan, DAST on staging, authorization test matrix. Tests shall include both malformed and adversarial inputs.

## Privacy/data governance
Data map: what is collected, why, retention, access and deletion; public filings distinct from user-entered potentially sensitive text. By default do not log full claims. Define provider contracts, storage region, incident response contacts, and subject-rights handling before collecting user data.

## Go-live blockers
Secrets in source/history; unrestricted data leakage; critical/high exploitable findings; unsupported citations; no rate limits at edge/shared store; unreviewed PII collection; missing alerting/rollback; public debug mode.
