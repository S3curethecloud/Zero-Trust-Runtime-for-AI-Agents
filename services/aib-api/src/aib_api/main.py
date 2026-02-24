from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pathlib import Path
import jwt

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from jwt.utils import base64url_encode

from .tokens import issue_token, KID

app = FastAPI(title="AIB Zero Trust Runtime")

KEYS_DIR = Path(__file__).resolve().parent.parent.parent / "keys" / "active"
PUBLIC_KEY_PATH = KEYS_DIR / "public.pem"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/token")
def create_token():
    token = issue_token("agent-1", {"risk": 10})
    return {"access_token": token}


def load_public_key():
    with open(PUBLIC_KEY_PATH, "rb") as f:
        key = serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )
    return key


def build_jwk(public_key):
    numbers = public_key.public_numbers()

    e = base64url_encode(
        numbers.e.to_bytes((numbers.e.bit_length() + 7) // 8, "big")
    ).decode("utf-8")

    n = base64url_encode(
        numbers.n.to_bytes((numbers.n.bit_length() + 7) // 8, "big")
    ).decode("utf-8")

    return {
        "kty": "RSA",
        "use": "sig",
        "kid": KID,
        "alg": "RS256",
        "n": n,
        "e": e,
    }


@app.get("/.well-known/jwks.json")
def jwks():
    public_key = load_public_key()
    jwk = build_jwk(public_key)
    return JSONResponse(content={"keys": [jwk]})
