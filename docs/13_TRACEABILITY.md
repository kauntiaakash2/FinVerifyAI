# Requirements, Verification Traceability & Release Evidence
Status: template; mark TODO until actual evidence exists.

| Requirement | Implementation target | Test evidence | Status |
|---|---|---|---|
| FR-01 typed extraction | parser/schema | unit + contract tests | TODO |
| FR-02 correct fiscal context | context matcher | golden FY/Q/YTD fixtures | TODO |
| FR-03 SEC citation provenance | evidence adapter | recorded + live bounded smoke | TODO |
| FR-04 numeric normalization | Decimal normalizer | unit/currency/rounding fixtures | TODO |
| FR-05 abstention correctness | verdict engine | adversarial benchmark | TODO |
| FR-06 typed API errors | HTTP contracts | 429/503/422 tests | TODO |
| FR-07 operability | telemetry/probes | staging alert/rollback evidence | TODO |
| FR-08 accessibility | UI | Playwright + manual review | TODO |
| FR-09 calibrated labels | UI/contracts | UI copy audit + evaluation | TODO |

## Evidence manifest
For each phase record commit SHA, commands, exit codes, test reports, coverage file, security scan, evaluation report, human review decision, documented limitations. NO guessed metrics. Mark unrun checks NOT RUN.

## Definition of Done
Working code + relevant tests + user documentation + risk assessment + traceability updates + reproducible evidence. A successful build is necessary but not sufficient for product quality or safe launch.
