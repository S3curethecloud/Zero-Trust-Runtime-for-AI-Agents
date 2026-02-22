from __future__ import annotations

from fastapi import APIRouter

from aib_api.models import TokenIntrospectRequest, TokenIntrospectResponse
from aib_api.tokens import introspect

router = APIRouter(prefix="/v1")


@router.post("/tokens:introspect", response_model=TokenIntrospectResponse)
def token_introspect(req: TokenIntrospectRequest):
    res = introspect(req.token)
    if not res.get("active"):
        return TokenIntrospectResponse(active=False, revoked=bool(res.get("revoked", False)))

    claims = res["claims"]
    return TokenIntrospectResponse(
        active=True and not bool(res.get("revoked", False)),
        revoked=bool(res.get("revoked", False)),
        session_id=str(claims.get("sid")) if claims.get("sid") else None,
        scope=list(claims.get("scope") or []),
        sub=str(claims.get("sub")) if claims.get("sub") else None,
        aud=str(claims.get("aud")) if claims.get("aud") else None,
        exp=int(claims.get("exp")) if claims.get("exp") else None,
        policy_rev=str(claims.get("policy_rev")) if claims.get("policy_rev") else None,
    )
