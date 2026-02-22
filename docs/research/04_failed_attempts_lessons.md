# Research — Failed Attempts / Lessons Learned

This project is explicitly designed to address recurring failure modes in agent systems.

## 1) Indirect prompt injection in tool-using agents
Peer-reviewed benchmarks show tool-integrated agents can be manipulated by malicious instructions embedded in external content.
- InjecAgent benchmark (ACL Findings): https://aclanthology.org/2024.findings-acl.624/

Implication:
- Treat external content + tool outputs as untrusted.
- Restrict agent capabilities with least-privilege tokens (AIB design).

## 2) Framework vulnerabilities (serialization / object injection)
CVE-2025-68664: LangChain serialization injection vulnerability enabling secret extraction.
- NVD: https://nvd.nist.gov/vuln/detail/CVE-2025-68664
- GitHub advisory: https://github.com/advisories/GHSA-c67j-w6g6-q2cm

Implication:
- Do not treat LLM-influenced structured data as trusted.
- Keep secrets out of agent-controlled memory/serialization paths.
- Enforce deterministic policy before issuing privileged credentials.

## 3) Government warnings on “never fully solved” prompt injection
UK NCSC notes prompt injection differs from SQL injection and should be treated as exploitation of an “inherently confusable deputy.”
- NCSC blog: https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection

Implication:
- Reduce impact by architectural controls (least privilege, PEPs, auditability).
