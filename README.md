# AI Request Triage on n8n

Portfolio project. A B2B request-triage workflow for a fictional AI and IT services agency (**Vértice IA**), built on a self-hosted n8n instance.

**Status: under construction.** Workflows, synthetic knowledge base, tests and evidence will be published here as each part is validated.

## What it will demonstrate

- Webhook intake with input validation and duplicate protection
- Context retrieval from PostgreSQL (service catalog, policies, SLAs, client plans)
- LLM classification and a structured draft reply, with deterministic validation of format and cited sources
- A deterministic fallback when the model is unavailable
- Authenticated, single-use human approval before anything leaves the system
- Error handling, execution receipts and a small evaluation set

## Boundaries

- Fictional company and synthetic data only. No real customer data.
- This is a portfolio project, not a production system.
- The workflow never sends a reply on its own: it prepares, a person approves.

## Author

Dyllan Alves — [Digytron](https://digytron.com)
