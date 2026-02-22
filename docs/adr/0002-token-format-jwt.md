# ADR 0002 — Token format is short-lived JWT (MVP)

## Status
Accepted

## Context
AIB must issue a credential that:
- Can be validated by PEPs without calling AIB (offline verification)
- Encodes scope and expiry
- Is short-lived and can be rotated

## Decision
Issue a **short-lived JWT** signed by AIB (MVP).

## Consequences
- PEPs must validate signature and enforce scope.
- For revocation before expiry, PEPs may introspect session revocation list (MVP).
- Enterprise: consider token exchange to cloud-native temporary credentials or integrate CAEP for continuous session attenuation.

## References
- RFC 8693 (Token Exchange): https://www.rfc-editor.org/rfc/rfc8693.html
- OpenID CAEP 1.0: https://openid.net/specs/openid-caep-1_0-final.html
