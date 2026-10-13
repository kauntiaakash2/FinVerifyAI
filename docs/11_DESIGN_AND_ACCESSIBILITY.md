# UX, Interface Design & Accessibility Specification
Status: prototype-ready design requirements, not final Figma mocks.

## Product principles
Evidence first; clear uncertainty; precision over flashy scoring; no finance-themed hype; no misleading confidence rings; professional typography, readable tables, context-rich links. Distinguish claim from extracted interpretation and from evidence.

## Information architecture
1 Claim submission; 2 extraction interpretation / edit ambiguity; 3 result with verdict and rationale; 4 supporting filing evidence; 5 coverage/limitations and data policy. History is optional opt-in.

## Key screen states
Empty input, typing, validating, resolving issuer, fetching filing, comparing, supported, contradicted, ambiguous with clarification, insufficient evidence, out of scope, rate limited, provider outage. Preserve user input and provide recoverable actions.

## Result page
Top: factual verdict, short explanation (not percentage). Then normalized claim vs evidence facts; fiscal period, unit, company CIK, data source, accession/filed date, relevant source URL and retrieval time; visible ambiguity and verification policy version.

## Interaction / a11y
WCAG 2.2 AA as design target: keyboard navigation, visible focus, 4.5:1 normal text contrast, accessible form errors, status region live announcements, no color-only status, responsive mobile cards, motion reduction, semantic HTML. Run axe/Playwright and targeted manual screen reader QA.

## Design system
Define tokens for type scale, spacing, neutrals, semantic statuses; use minimal data graphics. Charts must cite data dates and be optional/contextual (don't show share price trend as evidence for revenue claim). No real-company trademark impersonation.

## Usability evaluation
Five realistic verification tasks; measure success without coaching, time to source, misinterpretations and user trust calibration. Iterate evidence design before visual polish.
