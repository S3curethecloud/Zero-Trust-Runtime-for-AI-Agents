from __future__ import annotations

import time
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException

from aib_api import audit
from aib_api.auth import authenticate_agent
from aib_api.deterministic import input_hash
from aib_api.models import DecisionInput, PolicyMeta, TokenIssueRequest, TokenIssueResponse
from aib_api.opa import opa_client
from aib_api.risk import compute_risk_score
from aib_api.settings import settings
from aib_api.tokens import issue_token

router = APIRouter(prefix="/v1")


def _policy_meta() -> PolicyMeta:
    # MVP: fixed local policy revision.
    # Enterprise: compute bundle digest/revision from bundle server / OPA status.
    return PolicyMeta(bundle_revision="local-dev", bundle_digest=None)


@router.post("/tokens:issue", response_model=TokenIssueResponse)
async def issue(request: TokenIssueRequest, agent_sub: str = Depends(authenticate_agent)):
    # Derive agent identity deterministically:
    # - If agent auth is enabled, override body principal.agent_id with authenticated sub.
    # - If agent auth is disabled and agent_sub provided via header, override.
    principal = request.principal.model_copy(deep=True)
    if agent_sub:
        principal.agent_id = agent_sub

    # Deterministic risk normalization
    ctx = request.context.model_dump()
    ctx["risk_score"] = compute_risk_score(ctx)

    decision = DecisionInput(
        principal=principal,
        intent=request.intent,
        context=request.context.model_copy(update={"risk_score": ctx["risk_score"]}),
        policy=_policy_meta(),
    )

    di = decision.model_dump()
    ih = input_hash(di)

    opa_resp = await opa_client.decide(di)
    result = opa_resp.get("result") or {}
    allow = bool(result.get("allow", False))
    scopes = list(result.get("scopes") or [])
    ttl_seconds = int(result.get("ttl_seconds") or settings.jwt_ttl_seconds)
    obligations: Dict[str, Any] = dict(result.get("obligations") or {})

    audit.emit_audit_event(
        {
            "ts": int(time.time()),
            "request_id": request.context.request_id,
            "input_hash": ih,
            "policy_revision": decision.policy.bundle_revision,
            "principal": {"agent_id": principal.agent_id, "tenant_id": principal.tenant_id, "roles": principal.roles},
            "intent": {"action": request.intent.action, "resource": request.intent.resource.model_dump()},
            "decision": {"allow": allow, "scopes": scopes, "ttl_seconds": ttl_seconds, "obligations": obligations},
        }
    )

    if not allow:
        raise HTTPException(status_code=403, detail={"deny": True, "obligations": obligations, "input_hash": ih})

    token, sid, exp = issue_token(
        sub=principal.agent_id,
        scopes=scopes,
        policy_rev=decision.policy.bundle_revision,
        ttl_seconds=ttl_seconds,
        audience=settings.jwt_audience,
        issuer=settings.jwt_issuer,
    )

    return TokenIssueResponse(
        allow=True,
        token=token,
        expires_in=max(0, exp - int(time.time())),
        session_id=sid,
        scopes=scopes,
        obligations=obligations,
        input_hash=ih,
        policy_revision=decision.policy.bundle_revision,
    )
