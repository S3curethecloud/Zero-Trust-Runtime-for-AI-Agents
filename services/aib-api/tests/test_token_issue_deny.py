from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from aib_api.main import app


@pytest.mark.skip(reason="Integration test requires running OPA. Enable in CI with docker compose.")
def test_token_issue_deny():
    client = TestClient(app)
    payload = {
        "principal": {"agent_id": "agent:test", "tenant_id": "tenant:test", "roles": [], "assurance": "dev"},
        "intent": {"action": "refund:create", "resource": {"type": "reservation", "id": "X", "labels": {}}, "params": {"amount_usd": 9999}},
        "context": {"request_id": "req_1", "timestamp": "2026-02-22T00:00:00Z", "risk_score": 10, "signals": {}},
    }
    r = client.post("/v1/tokens:issue", json=payload)
    assert r.status_code == 403
