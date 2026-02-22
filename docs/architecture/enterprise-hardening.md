# Enterprise Hardening Plan

This document defines what “enterprise grade” means for AIB.

## Identity (agent authentication)
- Use workload identity (SPIFFE/SPIRE or platform-native workload identity)
- Avoid long-lived static secrets (replace with short-lived credentials)

SPIFFE defines a verifiable identity document (SVID) as a short-lived workload credential.

## Policy integrity
- Serve policies as bundles
- Sign bundles and verify signatures in OPA
- Version policies and record revision in every decision/audit record

OPA supports signed bundles and exposes bundle status/metadata.

## High availability
- AIB: stateless pods behind a load balancer
- OPA: deployed as sidecar per AIB instance OR as a replicated service
- Data stores for audit logs and revocations must be HA (e.g., multi-AZ)

## Key management
- Signing keys stored in KMS/HSM
- Key rotation with overlapping validity and key ids (kid)
- Support JWKS endpoint for PEPs

## Auditing and SIEM
- Decision logs + token issuance logs shipped to SIEM
- Immutable storage for compliance

## Continuous access (advanced)
- Integrate OpenID CAEP / SSF for continuous session revocation/attenuation
- Consider Token Exchange (RFC 8693) where interoperable with enterprise identity stacks

## Supply chain
- SBOM
- Signed container images
- SLSA-aligned build pipeline

## Compliance mapping (future)
- Map controls to NIST ZTA concepts
- Provide evidence artifacts per control (audit logs, policy revs, approvals)
