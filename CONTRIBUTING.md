# Contributing

## Workflow
1. Open an issue with a precise problem statement.
2. Add/Update an ADR in `docs/adr/` for any architectural change.
3. Ensure tests pass for `services/aib-api`.

## Coding rules (determinism)
- Authorization decisions must be derived from **explicit inputs**
- Never incorporate model outputs into authorization logic without a separate verification layer
