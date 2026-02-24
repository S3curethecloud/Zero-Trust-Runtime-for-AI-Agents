from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import jwt

from aib_api.tokens import load_public_key
from aib_api.session_store import is_session_active, revoke_session

router = APIRouter()


class IntrospectRequest(BaseModel):
    token: str


@router.post("/introspect")
def introspect(body: IntrospectRequest):
    public_key = load_public_key()

    try:
        payload = jwt.decode(
            body.token,
            public_key,
            algorithms=["RS256"],
        )
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    sid = payload.get("sid")
    if not sid:
        raise HTTPException(status_code=401, detail="Missing sid")

    if not is_session_active(sid):
        raise HTTPException(status_code=401, detail="Session revoked")

    return {
        "active": True,
        "sub": payload.get("sub"),
        "sid": sid,
        "exp": payload.get("exp"),
        "iat": payload.get("iat"),
    }


@router.post("/revoke/{sid}")
def revoke(sid: str):
    revoke_session(sid)
    return {"revoked": sid}
