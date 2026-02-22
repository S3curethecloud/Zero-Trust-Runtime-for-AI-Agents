# AIB API (FastAPI)

This service implements the **Agent Identity Broker** API:
- deterministic policy evaluation (via OPA)
- JIT token issuance
- session revocation + token introspection (MVP)

## Endpoints

- `GET /healthz`
- `POST /v1/tokens:issue`
- `POST /v1/tokens:introspect`
- `POST /v1/sessions/{sid}:revoke`

## Run locally (without docker)

```bash
pip install -r requirements.txt
uvicorn aib_api.main:app --reload --port 8080
```
