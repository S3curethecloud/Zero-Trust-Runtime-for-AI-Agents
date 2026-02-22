from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AIB_", extra="ignore")

    opa_url: str = "http://localhost:8181"
    opa_policy_path: str = "/v1/data/aib/decision"

    jwt_issuer: str = "aib.local"
    jwt_audience: str = "ztr-aa"
    jwt_ttl_seconds: int = 300

    # DEV ONLY: symmetric signing key. Enterprise should use KMS/HSM-managed asymmetric keys.
    signing_key_dev_only: str = "dev-secret-change-me"

    require_agent_auth: bool = False
    # DEV ONLY: if agent auth is required, accept a JWT signed with the same dev key.
    # Enterprise: replace with mTLS/SPIFFE or OIDC workload identity verification.
    agent_auth_audience: str = "aib"


settings = Settings()
