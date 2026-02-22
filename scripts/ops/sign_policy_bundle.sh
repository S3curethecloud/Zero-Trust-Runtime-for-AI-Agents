#!/usr/bin/env bash
set -euo pipefail

# Sign an OPA bundle (requires opa CLI installed and a signing key).
# Docs: https://www.openpolicyagent.org/docs/management-bundles
#
# Example:
#   opa build -b services/opa/policy -o dist/aib-bundle.tar.gz --signing-key <key>
#
echo "TODO: implement bundle signing workflow"
