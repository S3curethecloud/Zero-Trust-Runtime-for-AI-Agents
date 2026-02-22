from __future__ import annotations

import time
import uuid
from typing import Any, Dict, List, Optional, Tuple

import jwt

from aib_api.settings import settings


class SessionStore:
    """MVP in-memory store. Enterprise: replace with durable store (e.g., Redis)."""

    def __init__(self) -> None:
        self._revoked: set[str] = set()

    def revoke(self, session_id: str) -> None:
        self._revoked.add(session_id)

    def is_revoked(self, session_id: str) -> bool:
        return session_id in self._revoked


session_store = SessionStore()


def issue_token(
    sub: str,
    scopes: List[str],
    policy_rev: str,
    ttl_seconds: int,
    audience: str,
    issuer: str,
) -> Tuple[str, str, int]:
    now = int(time.time())
    exp = now + max(1, min(ttl_seconds, settings.jwt_ttl_seconds))
    sid = f"sid_{uuid.uuid4().hex}"

    claims: Dict[str, Any] = {
        "iss": issuer,
        "aud": audience,
        "sub": sub,
        "scope": scopes,
        "sid": sid,
        "policy_rev": policy_rev,
        "iat": now,
        "exp": exp,
    }

    token = jwt.encode(claims, settings.signing_key_dev_only, algorithm="HS256")
    return token, sid, exp


def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(
        token,
        settings.signing_key_dev_only,
        algorithms=["HS256"],
        audience=settings.jwt_audience,
        issuer=settings.jwt_issuer,
    )


def introspect(token: str) -> Dict[str, Any]:
    try:
        claims = decode_token(token)
    except Exception:
        return {"active": False, "revoked": False}

    sid = claims.get("sid")
    revoked = bool(sid and session_store.is_revoked(str(sid)))
    return {
        "active": True and not revoked,
        "revoked": revoked,
        "claims": claims,
    }
