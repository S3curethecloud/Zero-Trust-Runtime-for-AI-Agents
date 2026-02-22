# Agent Identity Broker (AIB) Architecture

This is the concrete architecture for the **Agent Identity Broker** used by the “Zero Trust Runtime for AI Agents”.

## Components

### 1) Agent Runtime (caller)
- The agent runtime (or agent tool wrapper) must submit **structured intent**, not free-form text.
- The agent runtime must include **agent identity** (workload identity) for authentication.

### 2) AIB API (this repo)
Responsibilities:
- Authenticate agent identity (MVP: optional; enterprise: required).
- Construct deterministic policy input and call PDP.
- Issue constrained, short-lived tokens.
- Persist decision + token issuance audit event.
- Provide revocation & introspection endpoints for PEPs.

### 3) Policy Decision Point (PDP)
- OPA (Open Policy Agent).
- Evaluates allow/deny and returns:
  - `allow: bool`
  - `scopes: string[]`
  - `ttl_seconds: int`
  - `obligations: object` (e.g., step-up, approvals, reason codes)

OPA supports decision logs including queried policy, input, and bundle metadata; and supports signed bundles for policy integrity.

### 4) Policy Bundle
- Versioned policy-as-code (Rego + data)
- Delivered as an OPA bundle
- Should be signed and verified by OPA for integrity

### 5) Policy Enforcement Point (PEP)
Where enforcement happens:
- API Gateway / Reverse proxy
- MCP server
- Sidecar in service mesh
- Custom SDK around tool APIs

PEP responsibilities:
- Verify AIB-issued token signature
- Enforce token scope
- Optionally introspect session revocation (MVP)
- Emit access logs with session id

## Request flow (token issuance)

1. Agent calls `POST /v1/tokens:issue`
2. AIB authenticates the agent (workload identity)
3. AIB canonicalizes the request into `DecisionInput` and computes `input_hash`
4. AIB calls OPA: `POST /v1/data/aib/decision`
5. OPA returns decision
6. AIB emits audit event and issues token (if allowed)

## Enforcement flow (tool call)

1. Agent calls a tool/connector behind a PEP
2. PEP verifies token + scope
3. PEP may call AIB introspection (optional / configurable)
4. Tool executes request

## Revocation flow (continuous access MVP)

1. AIB marks session revoked
2. PEP rejects future requests with that token/session id
3. Access is attenuated without waiting for token expiry (subject to PEP refresh/introspection cadence)

## Design constraints

- Authorization decision path is deterministic.
- No LLM is called in the authorization decision.
- Policy version/revision is always recorded.
