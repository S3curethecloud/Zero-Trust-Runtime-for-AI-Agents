from typing import Dict, Any, Tuple
from datetime import datetime, timezone, timedelta
from pathlib import Path
import uuid

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import jwt
from jwt import InvalidTokenError

# Keys stored at: services/aib-api/keys/active/
KEYS_DIR = Path(__file__).resolve().parent.parent.parent / "keys" / "active"
KID = "aib-key-1"

PRIVATE_KEY_PATH = KEYS_DIR / "private.pem"
PUBLIC_KEY_PATH = KEYS_DIR / "public.pem"


def load_private_key_pem() -> str:
    with open(PRIVATE_KEY_PATH, "r") as f:
        return f.read()


def load_public_key():
    with open(PUBLIC_KEY_PATH, "rb") as f:
        return serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )


def issue_token(
    subject: str,
    claims: Dict[str, Any],
    expires_minutes: int = 15
) -> Tuple[str, str]:
    """
    Issues an RS256 JWT and returns (token, sid).
    sid is a session identifier used for introspection + revocation.
    """
    private_key_pem = load_private_key_pem()
    sid = str(uuid.uuid4())

    now = datetime.now(timezone.utc)
    payload: Dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": now + timedelta(minutes=expires_minutes),
        "sid": sid,
        **claims,
    }

    token = jwt.encode(
        payload,
        private_key_pem,
        algorithm="RS256",
        headers={"kid": KID},
    )

    return token, sid


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verifies RS256 signature + standard claims.
    Returns: {"active": bool, "payload": dict|None}
    """
    public_key = load_public_key()
    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
        )
        return {"active": True, "payload": payload}
    except InvalidTokenError:
        return {"active": False, "payload": None}
