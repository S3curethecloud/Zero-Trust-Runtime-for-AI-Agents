from __future__ import annotations

from typing import Optional

import jwt
from fastapi import Header, HTTPException

from aib_api.settings import settings


def _bearer_token(authorization: Optional[str]) -> Optional[str]:
    if not authorization:
        return None
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1]


def authenticate_agent(
    authorization: Optional[str] = Header(default=None, alias="Authorization"),
    x_agent_id: Optional[str] = Header(default=None, alias="X-Agent-Id"),
) -> str:
    """Authenticate agent identity.

    Modes:
    - require_agent_auth=false (dev): accept X-Agent-Id or body principal
    - require_agent_auth=true: require Authorization Bearer JWT signed by dev key

    Enterprise: replace this with mTLS/SPIFFE/OIDC workload verification.
    """
    if not settings.require_agent_auth:
        if x_agent_id:
            return x_agent_id
        return ""

    token = _bearer_token(authorization)
    if not token:
        raise HTTPException(status_code=401, detail="Missing bearer token for agent auth")

    try:
        claims = jwt.decode(
            token,
            settings.signing_key_dev_only,
            algorithms=["HS256"],
            audience=settings.agent_auth_audience,
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid agent auth token")

    sub = claims.get("sub")
    if not sub:
        raise HTTPException(status_code=401, detail="Agent auth token missing sub")
    return str(sub)
