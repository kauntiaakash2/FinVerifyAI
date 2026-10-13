# QA, Verification & Release Test Strategy
Status: plan; no results implied.

## Pyramid
Unit: parser and normalizers, fiscal period matching, Decimal/tolerance comparator, verdict policy and errors.
Contract: SEC provider fixture parser, response schemas, version migrations.
Integration: SEC sandbox/recorded responses, DB transaction, cache, rate limiter.
E2E: browser user journey and citation drill-through with Playwright; keyboard/screen reader smoke coverage.
Non-functional: performance, fault injection, dependency timeout, security scans, structured logs.

## Golden fixtures
Correct historical filing; fiscal/calendar period mismatch; quarter vs YTD; USD vs non-USD; 0.20 ratio vs 20%; zero valid metric; revenue growth vs stock-price growth; amended filing; restatement; company alias; wrong CIK; unsupported concept; missing data; source API 429; malicious user input; fabricated SEC citation; stale cache; overflow/very large decimal; negative EPS; percentage-point phrasing.

## CI acceptance
Formatting/type checks, deterministic unit/contract/integration suites, security scans, API schema compatibility, fixture-backed evaluation subset, changed-file coverage checks, build artifacts. Do not call network APIs in hermetic unit tests. Pin requirements and lock dependency graph.

## Execution evidence
For each phase log exact commands, exit statuses, coverage and benchmark results, known skipped tests and why. A status marked PASS without logs is not acceptable.

## Release blocking criteria
Critical test failing, regression in false-support safety cases, missing citation link, exposure of secret, exploitable high-severity security issue, unbounded public endpoint abuse, inaccurate README claim, no rollback plan.
