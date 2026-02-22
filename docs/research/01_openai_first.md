# Research — OpenAI First

This project follows the mandatory sequence: **OpenAI docs first**.

## OpenAI resources used (security + agents)

1) Safety in building agents  
- Risk types and mitigation guidance for multi-agent workflows, including prompt injection and tool calling risks.  
https://developers.openai.com/api/docs/guides/agent-builder-safety

2) Function calling security  
- Security considerations for tool calling.  
https://platform.openai.com/docs/guides/function-calling/security

3) Apps SDK — Security & Privacy  
- Guidance: verify and enforce scopes on every tool call; reject expired/malformed tokens.  
https://developers.openai.com/apps-sdk/guides/security-privacy

4) Agents SDK  
- Framework concepts, including tools and tracing.  
https://developers.openai.com/api/docs/guides/agents-sdk  
https://openai.github.io/openai-agents-python/

5) MCP example guidance  
- Highlights that MCP can enforce consistent security and governance between model and tools.  
https://developers.openai.com/cookbook/examples/partners/mcp_powered_voice_agents/mcp_powered_agents_cookbook

## Extracted facts (for this project)

- OpenAI explicitly calls out prompt injection as a risk for agent workflows and suggests mitigation patterns.  
- Tool calling introduces additional risk; security must be applied at the tool boundary.
- Implementations should verify and enforce authorization scopes on tool calls.

(See the linked docs for details.)
