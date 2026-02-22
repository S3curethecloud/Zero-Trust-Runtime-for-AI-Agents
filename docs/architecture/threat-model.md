# Threat Model (AIB)

## Primary threats

### T1. Prompt injection → tool misuse
Risk: An attacker embeds malicious instructions in content the agent reads, causing unintended tool actions.
Mitigation:
- Treat agent as “confusable deputy”; reduce impact via least privilege tokens.
- Require structured intents and deny free-form tool access.
- Enforce per-action scope with short TTL.

Primary references:
- OWASP prompt injection guidance
- NCSC prompt injection “confusable deputy” framing
- OpenAI agent safety guidance (tool calling risk)

### T2. Token theft / replay
Risk: Attacker steals a short-lived token and replays requests.
Mitigation:
- Very short TTL
- Bind token to audience (aud) and scope
- Optional: bind to mTLS (enterprise)
- Revocation list / introspection
- Rate limits and anomaly detection

### T3. Policy tampering (supply chain)
Risk: Policy bundles modified to grant broader access.
Mitigation:
- Signed policy bundles verified by OPA
- Separate duties: policy authoring vs deployment
- Audit policy changes; immutable logs

### T4. Over-permissioned scopes
Risk: Policies too broad.
Mitigation:
- “Deny by default”
- “Narrow scopes” only
- Policy review + tests (policy unit tests)
- Use verifiable outcomes and “blast radius” constraints

### T5. Log tampering / missing provenance
Risk: No evidence chain for actions.
Mitigation:
- Append-only audit storage
- Include input_hash + policy_rev + token sid

## Trust boundaries

- Agent runtime is NOT trusted.
- Model outputs are NOT trusted.
- AIB and PDP are trusted components, but must be hardened.
- PEP is trusted to enforce (but must be observable and testable).
