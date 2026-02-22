# Zero Trust Runtime for AI Agents

**Repo:** `zero-trust-runtime-for-ai-agents`  
**Primary component:** Agent Identity Broker (AIB)

This repository is a **build-ready skeleton** for an **Agent Identity Broker** that issues **Just-in-Time (JIT), least-privilege credentials** to AI agents (non-human identities) and enables **deterministic, auditable enforcement** at the agent↔tool boundary.

> Marketing name: **Zero Trust Runtime for AI Agents** (ZTR-AA)

## What this is

An Agent Identity Broker (AIB) that:
- Authenticates an agent workload (machine identity)
- Accepts an *explicit* `intent` request (structured, not natural language)
- Evaluates access *deterministically* via an external policy engine (OPA)
- Issues a short-lived token with bounded scope
- Emits audit evidence linking **(intent → policy decision → issued credential)**

## What this is NOT

- Not a prompt-based “guardrail” product
- Not an LLM wrapper
- Not an autonomy platform
- Not a SIEM

## Start (local dev)

Prereqs: Docker + Docker Compose.

```bash
docker compose up --build
```

Then:

```bash
curl -s http://localhost:8080/healthz | jq
```

## Repo map (high level)

- `services/aib-api/` — FastAPI service that implements deterministic broker logic
- `services/opa/` — Open Policy Agent policy + config (deterministic PDP)
- `docs/` — Source of truth, threat model, policy model, research notes
- `examples/` — Example agent client + MCP server stub
- `infra/` — K8s manifests (base + overlays)

## Governance (MGF-ALPHA)

See:
- `GOVERNANCE.md`
- `docs/SOURCE_OF_TRUTH.md`

## License

See `LICENSE`.
