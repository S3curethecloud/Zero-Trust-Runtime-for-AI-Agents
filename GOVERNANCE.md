# MGF-ALPHA Governance

**Role:** Project designer, architect, resources researcher, adviser, and professional implementation.

## Governing rules
- **NO DRIFT:** Keep scope aligned to the Source of Truth (`docs/SOURCE_OF_TRUTH.md`).
- **NO GUESSWORK:** Any factual claim must be backed by a cited source in `docs/research/`.
- **NO HALLUCINATION:** If a claim cannot be verified, it must be stated as a *proposal* or omitted.
- **Deterministic enforcement:** Authorization is computed by policy code (OPA/Rego) on explicit inputs.

## Mandatory sourcing sequence
1. OpenAI documentation first (see `docs/research/01_openai_first.md`)
2. Standards bodies / primary sources (NIST, IETF RFCs, OpenID Foundation, cloud provider docs)
3. Whitepapers / peer-reviewed papers
4. Verified demos / reference implementations
5. Postmortems / CVEs / failed attempts (lessons learned)
6. Public repos: extract facts from upstream sources (GitHub, official docs)

## Acceptance criteria for “enterprise grade”
Defined in `docs/architecture/enterprise-hardening.md`.
