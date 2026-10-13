# Operations, SRE & Deployment Readiness
Status: design plan; deployment is not yet verified.

## Environments
Development (fixtures), staging (real SEC requests with quotas), production. Isolated configuration, no production secrets in preview branches. Explicit immutable build IDs and database migration checks.

## SEC data ingestion
Use SEC data.sec.gov and filing documents subject to current SEC policies; identify requests with a descriptive user agent, adhere to fair access and rate limits, back off on 429, do not promise real-time regulatory data. Cache based on filings and provenance. Review terms/licensing before commercial usage. API schemas and current limits must be verified immediately before launch.

## Observability
Metrics: verification verdict distribution; supported/abstained ratio; upstream failures; citation resolution errors; p50/p95; latency by stage; cache hit; 429 counts; error budget; extraction drift; server resource utilization.
Alerts: elevated 5xx, anomalous 429, evidence provider outage, false-support regression from synthetic probes, queue backlog, expiry of secrets/certs.

## Backup & recovery
If using DB: automated encrypted backup, restore exercise, defined RPO/RTO after host choice, migration rollback compatibility, documented deletion/retention. Do not promise unattested backup.

## Release procedure
Tag candidate -> CI/security/evaluation -> deploy staging -> smoke, load and security tests -> approval -> canary/small rollout -> production synthetic probes -> monitor -> rollback if threshold breached.

## Incident response
Severity classification, on-call owner, containment, disable-verification feature flag, revoke compromised credentials, evidence integrity recheck, postmortem timeline.

## Launch checklist
No known critical/high vulnerabilities; no debug mode; verified allowed origins; secrets rotated; correct 429/503 semantics; health/readiness probes; source URLs valid; legal/privacy notice; monitoring dashboards; rollback rehearsed; known limitations and unsupported claim types prominently disclosed.
