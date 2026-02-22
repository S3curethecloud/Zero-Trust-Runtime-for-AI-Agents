from __future__ import annotations

import json
import uuid
import requests
from datetime import datetime, timezone

AIB = "http://localhost:8080"

payload = {
    "principal": {
        "agent_id": "agent:refund-bot",
        "tenant_id": "tenant:united-demo",
        "roles": ["refund_agent"],
        "assurance": "dev",
    },
    "intent": {
        "action": "refund:create",
        "resource": {"type": "reservation", "id": "ABC123", "labels": {"channel": "web"}},
        "params": {"amount_usd": 120.50, "currency": "USD"},
    },
    "context": {
        "request_id": f"req_{uuid.uuid4().hex}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "risk_score": 42,
        "signals": {},
    },
}

r = requests.post(f"{AIB}/v1/tokens:issue", json=payload, timeout=5)
print("status:", r.status_code)
print(json.dumps(r.json(), indent=2))
