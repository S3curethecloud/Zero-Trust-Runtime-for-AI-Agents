from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Principal(BaseModel):
    agent_id: str = Field(..., description="Stable agent identity (NHI).")
    tenant_id: str = Field(..., description="Tenant / trust domain.")
    roles: List[str] = Field(default_factory=list)
    assurance: str = Field("dev", description="How the agent was authenticated (mTLS/SPIFFE/JWT/etc).")


class Resource(BaseModel):
    type: str
    id: str
    labels: Dict[str, Any] = Field(default_factory=dict)


class Intent(BaseModel):
    action: str
    resource: Resource
    params: Dict[str, Any] = Field(default_factory=dict)


class Context(BaseModel):
    request_id: str
    timestamp: str  # ISO8601 string
    risk_score: int = 0
    signals: Dict[str, Any] = Field(default_factory=dict)


class PolicyMeta(BaseModel):
    bundle_revision: str
    bundle_digest: Optional[str] = None


class DecisionInput(BaseModel):
    principal: Principal
    intent: Intent
    context: Context
    policy: PolicyMeta


class TokenIssueRequest(BaseModel):
    principal: Principal
    intent: Intent
    context: Context


class TokenIssueResponse(BaseModel):
    allow: bool
    token: Optional[str] = None
    expires_in: Optional[int] = None
    session_id: Optional[str] = None
    scopes: List[str] = Field(default_factory=list)
    obligations: Dict[str, Any] = Field(default_factory=dict)
    input_hash: str
    policy_revision: str


class TokenIntrospectRequest(BaseModel):
    token: str


class TokenIntrospectResponse(BaseModel):
    active: bool
    revoked: bool
    session_id: Optional[str] = None
    scope: List[str] = Field(default_factory=list)
    sub: Optional[str] = None
    aud: Optional[str] = None
    exp: Optional[int] = None
    policy_rev: Optional[str] = None
