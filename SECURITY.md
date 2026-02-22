# Security Policy

## Reporting
If you discover a vulnerability, **do not** open a public issue.
Instead, contact the maintainers privately.

## Scope (initial)
- `services/aib-api`
- `services/opa` policies and config
- `infra` manifests

## Principles
- No long-lived shared secrets for agent workloads (use short-lived credentials)
- Deterministic authorization decisions (no LLM in the decision path)
- Every decision is auditable (input, policy revision, output)
