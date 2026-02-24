from typing import Dict, Any
from datetime import datetime, timezone, timedelta
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import jwt
from jwt import InvalidTokenError

# NOTE: KEYS_DIR and KID must be defined in your project scope.
# If your project already defines these above, keep them there and remove duplicates.
KEYS_DIR = Path(__file__).resolve().parent / "keys"
KID = "aib-key-1"

PRIVATE_KEY_PATH = KEYS_DIR / "private.pem"
PUBLIC_KEY_PATH = KEYS_DIR / "public.pem"


def load_private_key() -> str:
    with open(PRIVATE_KEY_PATH, "r") as f:
        return f.read()


def load_public_key():
    with open(PUBLIC_KEY_PATH, "rb") as f:
        return serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )


# ---- Revocation Store ----
REVOKED_TOKENS = set()


def revoke_token(token: str):
    REVOKED_TOKENS.add(token)


def is_revoked(token: str) -> bool:
    return token in REVOKED_TOKENS


def issue_token(subject: str, claims: Dict[str, Any], expires_minutes: int = 15) -> str:
    private_key = load_private_key()

    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "iat": now,
        "exp": now + timedelta(minutes=expires_minutes),
        **claims,
    }

    token = jwt.encode(
        payload,
        private_key,
        algorithm="RS256",
        headers={"kid": KID},
    )

    return token


def verify_token(token: str):
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
