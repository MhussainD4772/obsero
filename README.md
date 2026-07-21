# Obsero

**Open-source, self-hostable observability and evaluation for LLM applications.**

Obsero gives you visibility into what happens inside AI features: which prompts are slow, which calls cost the most, and whether a model or prompt change silently degraded output quality.

## What it does

- **Ingest** — wrap LLM calls with the Python SDK; capture prompt, response, tokens, latency, cost, and model
- **Trace** — nested spans so you can see the full path of a request
- **Analyze** — cost and latency dashboards
- **Evaluate** — score prompts and models against saved datasets with LLM-as-judge

## Stack

| Layer | Tech |
|-------|------|
| SDK | Python, httpx |
| Backend | FastAPI, async SQLAlchemy, Pydantic v2 |
| Database | PostgreSQL |
| Worker | Background tasks → arq/Redis |
| Dashboard | Next.js (App Router), TypeScript, Tailwind, TanStack Query |
| Infra | Docker Compose (`docker compose up`) |

## Status

Early development. Scaffolding and first vertical slice (ingest → store → list) are in progress.

## License

TBD
