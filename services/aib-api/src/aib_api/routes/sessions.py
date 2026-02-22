from __future__ import annotations

from fastapi import APIRouter

from aib_api.tokens import session_store

router = APIRouter(prefix="/v1")


@router.post("/sessions/{sid}:revoke")
def revoke(sid: str):
    session_store.revoke(sid)
    return {"revoked": True, "session_id": sid}
