package aib

default decision = {
  "allow": false,
  "scopes": [],
  "ttl_seconds": 0,
  "obligations": {"reason_codes": ["DENY_DEFAULT"]}
}

# ---- Helpers ----

has_role(role) if {
  role == input.principal.roles[_]
}

amount_usd := input.intent.params.amount_usd

# ---- Allow rules ----

# Example: allow refund:create for refund_agent with bounded amount + risk score
decision = {
  "allow": true,
  "scopes": ["refund:create"],
  "ttl_seconds": 300,
  "obligations": {"reason_codes": ["ROLE_MATCHED", "AMOUNT_OK", "RISK_OK"]}
} if {
  input.intent.action == "refund:create"
  has_role("refund_agent")
  amount_usd <= 500
  input.context.risk_score <= 70
}

# Example: allow refund:read to a broader role
decision = {
  "allow": true,
  "scopes": ["refund:read"],
  "ttl_seconds": 300,
  "obligations": {"reason_codes": ["ROLE_MATCHED"]}
} if {
  input.intent.action == "refund:read"
  has_role("support_agent")
}
