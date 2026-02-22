# Deterministic Enforcement Logic

This document defines what “deterministic enforcement” means for AIB.

## Definition

An authorization decision is deterministic if:
- It is computed by policy code on explicit, well-typed inputs.
- The same inputs + same policy revision → same decision.
- No probabilistic model output is used as an authorization signal.

## Inputs (explicit)

Decision input is the canonical JSON object:

- `principal` (agent identity)
  - `agent_id`
  - `tenant_id`
  - `roles` (string[])
  - `assurance` (e.g., mTLS/SPIFFE/JWT issuer)

- `intent`
  - `action` (verb)
  - `resource`
    - `type`
    - `id`
    - `labels` (optional)
  - `params` (typed parameters; never free-form)
  - `justification` (optional, but should be constrained)

- `context`
  - `request_id`
  - `timestamp` (ISO 8601)
  - `risk_score` (0-100, deterministic function or provided by risk system)
  - `signals` (optional)

- `policy`
  - `bundle_revision`
  - `bundle_digest` (if available)

## Canonicalization

AIB MUST:
- sort JSON object keys recursively
- encode using UTF-8
- remove non-deterministic fields from the input unless explicitly included

Then compute:
`input_hash = SHA256(canonical_json)`

## PDP call

OPA is called with:

```json
{
  "input": { ...DecisionInput... }
}
```

OPA returns:

```json
{
  "result": {
    "allow": true,
    "scopes": ["refund:create"],
    "ttl_seconds": 300,
    "obligations": {
      "reason_codes": ["LOW_RISK", "ROLE_MATCHED"]
    }
  }
}
```

## Token issuance

If allow:
- issue JWT with:
  - `sub` agent_id
  - `aud` target PEP/audience
  - `scope` scopes
  - `exp` now + ttl_seconds (bounded by broker maximum)
  - `sid` session id
  - `policy_rev` bundle_revision

## Audit event (minimum fields)

- `timestamp`
- `request_id`
- `principal.agent_id`
- `intent.action`
- `intent.resource`
- `input_hash`
- `policy.bundle_revision`
- `decision.allow`
- `decision.scopes`
- `token.sid` (if issued)

OPA can emit decision logs containing input and bundle metadata; AIB should store the OPA decision id (if available) or the full decision record.

## Security note

This design explicitly treats model outputs as untrusted and constrains agent capabilities via least-privilege credentials.
