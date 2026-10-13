# Risk Register
Status: initial; update each phase. Severity denotes consequence, not observed exploit.

| ID | Risk | Severity | Early signal | Mitigation | Owner |
|---|---|---|---|---|---|
| R1 | Historical figures compared to current metrics | Critical | false contradictions | period-specific SEC facts & golden tests | verification lead |
| R2 | Wrong semantic metric or fiscal concept | Critical | wrong evidence selected | governed taxonomy & abstain | finance/domain reviewer |
| R3 | False confidence / fabricated citations | Critical | unsupported result shown as verified | deterministic verdict, provenance validation | AI lead |
| R4 | SEC rate limits/outages | High | 429, timeout | fair-access client, bounded retries, cache | backend lead |
| R5 | Incomplete or restated filings | High | conflicting annual facts | as-of policy & amendment linkage | data lead |
| R6 | Exposure of claim text and credentials | High | secrets/log leakage | minimize logging, secret manager, threat tests | security lead |
| R7 | Prompt injection if LLM introduced | High | model follows document commands | strict untrusted-data boundary | AI lead |
| R8 | No real user need | High | no repeat pilots | interviews and competitor benchmark | product lead |
| R9 | Unfair or misleading investment interpretation | High | users assume advice | clear limited scope and verdict semantics | product lead |
| R10 | Over-scoping into agents/blockchain/PDFs | High | slipping correctness milestones | gate optional features | maintainer |
| R11 | Non-deterministic online tests | Medium | flaky CI | offline recorded fixtures | QA lead |
| R12 | Third-party service costs/terms change | Medium | quota/license changes | provider abstraction, budget, legal review | maintainer |
