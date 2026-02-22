# SOURCE OF TRUTH — Zero Trust Runtime for AI Agents (ZTR-AA)

This document is the **single source of truth** for the Agent Identity Broker (AIB) scope, concepts, architecture, and enterprise hardening path.

## 0. Terms (precise)

- **Agent**: An automated workload that can request actions against protected resources (APIs, tools, SaaS, data).
- **Agent Identity Broker (AIB)**: A service that issues short-lived, least-privilege credentials to agents after deterministic policy evaluation.
- **Intent**: A structured request describing *what action* is being attempted, *on what resource*, and *why* (never free-form text).
- **PDP**: Policy Decision Point (authorization decision service).
- **PEP**: Policy Enforcement Point (enforces the authorization decision near the resource).
- **JIT identity**: Just-in-time credentials with a narrowly scoped permission set and short lifetime.
- **CAE/CAEP**: Continuous Access Evaluation / OpenID Continuous Access Evaluation Profile, used to revoke or attenuate access during a session.

## 1. Problem (why AIB exists)

AI agents are exposed to **prompt injection** and related instruction/data confusion. OWASP describes prompt injection as a vulnerability where attackers manipulate model behavior via crafted input, exploiting the lack of clear separation between “instructions” and “data.” (See OWASP LLM Prompt Injection Prevention Cheat Sheet.)

The UK NCSC warns that prompt injection should be viewed as exploitation of an “inherently confusable deputy” and advises focusing on **secure system design** that reduces impact rather than relying on “silver bullet” mitigations. (See NCSC prompt injection blog/pdfs.)

OpenAI’s guidance on building agents highlights prompt injection risk and emphasizes caution around tool calling (including MCP tool calling). (See OpenAI “Safety in building agents”.)

**Therefore:** security controls for agent actions must sit **outside** the model and be **deterministic**.

## 2. Objective (what we build)

Build an Agent Identity Broker that:
1. Authenticates the calling agent (workload identity)
2. Receives an explicit, structured intent (action/resource/parameters)
3. Evaluates access deterministically using a policy engine
4. Issues a short-lived credential constrained to the allowed scope
5. Emits an audit trail linking: intent → policy revision → decision → credential
6. Supports revocation / continuous access controls (initially via short TTL + broker-side revocation list; later CAEP/SSF integration)

## 3. Non-goals (explicit)

- We are not building an LLM “alignment” or safety classifier.
- We are not building a vertical agent or orchestration framework.
- We are not replacing enterprise IdPs (Okta/Entra/AD) — we integrate with them.

## 4. Architecture (conceptual)

**Core components**
- **AIB API** (this repo): deterministic decision orchestration + token issuance.
- **Policy Engine (PDP)**: Open Policy Agent (OPA) queried by AIB for decisions.
- **Policy Bundle**: versioned policy-as-code, ideally signed and delivered as an OPA bundle.
- **PEP**: enforced at tool boundary (e.g., API gateway, MCP server, sidecar) verifying AIB-issued token.
- **Audit Log Sink**: immutable decision logs + token issuance logs.

**Why OPA?**
OPA supports decision logs that include queried policy, input, and bundle metadata (enables audit/debug). OPA also supports signed bundles for integrity of delivered policy bundles.

## 5. Deterministic enforcement logic (definition)

AIB enforcement MUST be deterministic:
- No LLM is called during authorization.
- Decision is derived from explicit inputs:
  - agent identity (principal)
  - intent (action/resource)
  - context (risk score, tenant, time, device posture signals, etc.)
  - policy revision (bundle digest/revision)

**Pipeline**
1. Authenticate agent (mTLS / SPIFFE SVID / JWT from trusted issuer)
2. Normalize + canonicalize decision input; compute `input_hash = SHA256(canonical_json)`
3. Call PDP: `POST /v1/data/aib/decision` with `{ "input": <DecisionInput> }`
4. PDP returns: `{ allow, scopes, ttl, obligations }`
5. If allow: issue JWT with:
   - `sub`: agent_id
   - `aud`: target audience (tool/proxy)
   - `scope`: scopes from policy
   - `exp`: now + ttl (bounded)
   - `sid`: session id
   - `policy_rev`: policy revision id
6. Persist audit record with: input_hash, decision, policy_rev, token metadata, timestamp
7. Return token and obligations to caller

## 6. Continuous access (concept-to-enterprise path)

**MVP**
- Short-lived tokens (5 minutes)
- Broker-side revocation list (session_id → revoked)
- PEP checks token + introspects revocation periodically

**Enterprise**
- Integrate CAEP/SSF for continuous session attenuation/revocation
- Use cloud-native temporary credentials (e.g., AWS STS) where possible instead of custom JWT
- Workload identity using SPIFFE/SPIRE, or platform-native workload identity (K8s, cloud)

Microsoft Entra’s Continuous Access Evaluation references CAEP as the underlying standard profile. CAEP (OpenID Foundation) defines event types for continuous updates between transmitters and receivers.

## 7. Why “failed attempts” matter (lessons)

Frameworks and agent runtimes can be vulnerable when untrusted, LLM-influenced data is treated as trusted. For example, CVE-2025-68664 in LangChain involved a serialization injection vulnerability in dumps()/dumpd() where internal markers were not escaped, enabling secret extraction.

AIB design principle:
- treat all model output as untrusted
- enforce *capabilities* via tokens and PEPs, not via “trusting outputs”
- log every decision with provenance (policy revision + input hash)

## 8. References (primary)

OpenAI (start here)
- OpenAI — Safety in building agents: https://developers.openai.com/api/docs/guides/agent-builder-safety
- OpenAI — Function calling security: https://platform.openai.com/docs/guides/function-calling/security
- OpenAI — Apps SDK Security & Privacy: https://developers.openai.com/apps-sdk/guides/security-privacy
- OpenAI — Agents SDK overview: https://developers.openai.com/api/docs/guides/agents-sdk

Standards / Gov
- NIST SP 800-207 Zero Trust Architecture: https://csrc.nist.gov/pubs/sp/800/207/final
- NCSC blog: “Prompt injection is not SQL injection”: https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection
- OWASP LLM Prompt Injection Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html

Identity / session standards
- RFC 8693 OAuth 2.0 Token Exchange: https://www.rfc-editor.org/rfc/rfc8693.html
- OpenID CAEP 1.0 (final): https://openid.net/specs/openid-caep-1_0-final.html

Workload identity
- SPIFFE concepts: https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/

Policy engine
- OPA Decision Logs: https://www.openpolicyagent.org/docs/management-decision-logs
- OPA Signed Bundles: https://www.openpolicyagent.org/docs/management-bundles

Public “failed attempt” evidence
- NVD CVE-2025-68664: https://nvd.nist.gov/vuln/detail/CVE-2025-68664
- GitHub Advisory GHSA-c67j-w6g6-q2cm: https://github.com/advisories/GHSA-c67j-w6g6-q2cm
