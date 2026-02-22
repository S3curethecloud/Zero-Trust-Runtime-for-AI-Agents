# ADR 0001 — Use OPA as the Policy Decision Point

## Status
Accepted

## Context
We need a deterministic authorization engine that:
- Evaluates allow/deny from explicit inputs
- Produces audit/debug artifacts (policy version, input, decision)
- Supports integrity for policy distribution

## Decision
Use **Open Policy Agent (OPA)** as the PDP.

## Consequences
- Policies are authored as Rego + data and shipped as bundles.
- AIB queries OPA via HTTP API for every token issuance decision.
- We can use OPA decision logs and bundle metadata for auditing.

## References
- OPA Decision Logs: https://www.openpolicyagent.org/docs/management-decision-logs
- OPA Bundles (including signed bundles): https://www.openpolicyagent.org/docs/management-bundles
