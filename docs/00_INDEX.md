# FinVerify — Rebuild Documentation Index
Status: Draft for review; baseline 2026-10-13. Owner: repository maintainer.

## Decision
Rebuild as a **filing-backed, period-aware, evidence-grounded financial claim verifier**, not a live quote comparator. Start with US SEC reporting and a small, explicitly supported coverage set. Avoid declaring production-ready before gates pass. Not investment advice.

## Documents and sequence
1. 01_PRD.md — target users, use cases, functional requirements, exclusions, acceptance criteria.
2. 02_DISCOVERY_AND_VALIDATION.md — user interviews, competitor analysis, go/no-go evidence.
3. 03_SYSTEM_DESIGN.md — components, boundaries, flows, scaling, decisions.
4. 04_FINANCIAL_SEMANTICS.md — verification contract, periods, currency, units, failures.
5. 05_DATA_MODEL_AND_API.md — entities, endpoints, state and response schemas.
6. 06_SECURITY_AND_PRIVACY.md — threat model and enforceable controls.
7. 07_AI_AND_EVALUATION.md — datasets, model boundaries, benchmarks, metrics.
8. 08_QA_TEST_STRATEGY.md — test matrix and quality gates.
9. 09_OPERATIONS_AND_DEPLOYMENT.md — deployment, monitoring, backup, rollback.
10. 10_PHASE_PLAN_AND_ADRS.md — roadmap, dependencies, exit criteria, ADR register.
11. 11_DESIGN_AND_ACCESSIBILITY.md — product UX, accessibility, UI states.
12. 12_RISK_REGISTER.md — risks, triggers, owners, mitigations.
13. 13_TRACEABILITY.md — requirement-to-test map and evidence checklist.
14. prompts/MASTER_REBUILD_PROMPT.md — copy/paste agent execution prompt.

## Source of truth
Treat README and old code as **claims to verify**, not authoritative truth. Every document contains proposed requirements, not implementation evidence. Update each status and attach test outputs and ADRs as you progress.

## References
- SEC data APIs: https://data.sec.gov/ and https://www.sec.gov/edgar/sec-api-documentation
- SEC developer and fair-access guidance: https://www.sec.gov/developer
- OWASP ASVS 5: https://owasp.org/www-project-application-security-verification-standard/
- OWASP API Security: https://owasp.org/www-project-api-security/
- NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework
