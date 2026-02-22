from __future__ import annotations

from typing import Any, Dict

import httpx

from aib_api.settings import settings


class OpaClient:
    def __init__(self, base_url: str, policy_path: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.policy_path = policy_path

    async def decide(self, decision_input: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{self.policy_path}"
        payload = {"input": decision_input}
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            return r.json()


opa_client = OpaClient(settings.opa_url, settings.opa_policy_path)
