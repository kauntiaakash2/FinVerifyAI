# Phase Plan, Dependencies & Architecture Decision Records
Status: proposed sequence. Phase completion requires evidence, not declarations.

## Phase 0 — Audit, protect, establish baseline
Read full repository, commit state, routes, dependencies, README claims, tests, deployment. Create feature branch; no destructive rewrite. Snapshot API and run tests. Produce REPO_AUDIT.md with claim-vs-code matrix and issues by severity. Gate: reviewable baseline and reproducible commands.

## Phase 1 — Discovery + requirements lock
Interview candidate users, evaluate alternatives; approve PRD, user journeys, supported issuer/metric matrix, semantics, threat model. Gate: documented use-case priority and unresolved assumptions called out.

## Phase 2 — Domain correctness foundation
Refactor into ports/adapters; implement CIK registry, canonical Decimal model, period concepts, deterministic verdicts and abstention. Record golden tests. Gate: all critical unit/context fixtures pass.

## Phase 3 — SEC evidence ingestion
Implement SEC API adapter with identity, rate control, provenance, filing URLs, amendments and cache; mocked tests and constrained live smoke. Gate: source-backed fixture cases with accurate filing links and graceful 429/unavailable handling.

## Phase 4 — Evaluation-first extraction
Implement baseline extractor; curate and version labeled dataset; optionally integrate structured LLM extractor only if improvement measured. Gate: frozen test metrics, traceable errors, no silent hallucinated company/period/metric.

## Phase 5 — MVP UX and API
User input, status states, evidence comparison, coverage disclosure, accessible responsive layout, typed API/OpenAPI, citation drill-down; optional history only with privacy model. Gate: E2E and accessibility suite pass.

## Phase 6 — Reliability, security and performance
Shared throttling, secure headers, strict CORS, schema validation, timeouts, dependency and secret scans, observability, caching and load tests. Gate: no unaddressed critical/high issues and recorded perf results.

## Phase 7 — Staging, beta and production
Staging deployment, migrations/backup if relevant, incident drills, real user pilot, corrections, production deployment with monitoring and rollback. Gate: signed release checklist and evaluated, honestly scoped README.

## Phase 8 — Optional expansion, never prerequisite to correctness
Batch ingestion, PDFs, 10-Q quarter derivations, broader issuers, explanatory AI, other jurisdictions. Each feature needs renewed threat/data/benchmark review.

## ADR template
ADR-ID, title, status, context/problem, options, decision, rationale, downsides, security/privacy impact, cost, reversal trigger, date, owner. No silent stack upgrades or architecture pivots.

## Stop conditions
If testing fails or external data terms make design infeasible, stop and document blocker + safe alternative. Never assert deployment, correctness or benchmarking without direct evidence.
