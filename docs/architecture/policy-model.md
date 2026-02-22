# Policy Model

This repo ships a minimal Rego policy (`services/opa/policy/aib.rego`) as a starting point.

## Schema (DecisionInput)

```json
{
  "principal": {
    "agent_id": "agent:refund-bot",
    "tenant_id": "tenant:united-demo",
    "roles": ["refund_agent"],
    "assurance": "dev-jwt"
  },
  "intent": {
    "action": "refund:create",
    "resource": {
      "type": "reservation",
      "id": "ABC123",
      "labels": {"channel": "web"}
    },
    "params": {
      "amount_usd": 120.50,
      "currency": "USD"
    }
  },
  "context": {
    "request_id": "req_123",
    "timestamp": "2026-02-22T10:00:00Z",
    "risk_score": 42
  },
  "policy": {
    "bundle_revision": "local-dev",
    "bundle_digest": "sha256:..."
  }
}
```

## Policy outputs

OPA returns:

- allow/deny
- scopes
- ttl
- obligations

Obligations can include:
- required approvals (HITL)
- reason codes
- required step-up auth

## Determinism requirements

Policy must:
- be a pure function of `input`
- avoid calls to external systems
- avoid randomness

## Policy testing

Add policy unit tests in the future:
- `opa test` for Rego unit tests
- golden tests with fixed DecisionInput fixtures
