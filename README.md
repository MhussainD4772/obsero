# Obsero

[![CI](https://github.com/MhussainD4772/obsero/actions/workflows/ci.yml/badge.svg)](https://github.com/MhussainD4772/obsero/actions/workflows/ci.yml)

**Open-source, self-hostable observability for LLM applications.**

---

## What is Obsero?

Obsero helps you see inside AI features in production and development.

When you ship a chatbot, agent, or any LLM-powered flow, most of the important work happens in black-box API calls. You don’t get a clear answer to:

- Which prompts are slow?
- Which calls cost the most?
- Did a model or prompt change silently hurt quality?

Obsero closes that gap. You wrap your existing LLM calls with a small SDK. Obsero records what happened — prompt, response, model, tokens, latency, and cost — stores it on infrastructure you control, and shows it in a dashboard.

Your data stays with you. No SaaS lock-in required.

---

## How it works

```
Your app
   │
   │  wrap LLM calls with the Obsero SDK
   ▼
Obsero backend (FastAPI)
   │
   ▼
PostgreSQL
   │
   ▼
Dashboard (Next.js)
```

1. **Instrument** — Install the Python SDK and wrap chat/completions (or use the `trace` helper around any provider).
2. **Capture** — Each call ships prompt, response, tokens, latency, estimated cost, and model metadata.
3. **Store** — The self-hosted API writes events to Postgres (single events or batched).
4. **Inspect** — Open the dashboard to browse calls, costs, and latency, and expand a row for full input/output.

If the Obsero backend is down, the SDK fails soft — your app keeps running.

---

## End goal

Obsero aims to be the self-hosted control plane for LLM apps:

| Pillar | Goal |
|--------|------|
| **Ingestion & tracing** | Reliable capture of LLM calls, including nested spans for multi-step agents |
| **Analytics** | Cost and latency trends you can act on after every model or prompt change |
| **Evaluation** | Datasets + LLM-as-judge so quality regressions show up before users do |
| **Teams & auth** | Projects, access control, and one-command self-host for real teams |

Today the foundation is live: ingest → store → dashboard for real LLM calls. The product roadmap is to grow that into full tracing, analytics, and evals — still open source, still self-hostable.

---

## Quick start

```bash
git clone https://github.com/MhussainD4772/obsero.git
cd obsero
docker compose up -d
```

| Service | URL |
|---------|-----|
| API health | http://localhost:8000/health |
| Dashboard | http://localhost:3000 (`cd frontend && npm ci && npm run dev`) |

Send a test event:

```bash
pip install -e ./sdk
python -c "import obsero; obsero.track('hello', {'ok': True})"
```

Then refresh the dashboard.

---

## Stack

| Layer | Technology |
|-------|------------|
| SDK | Python, httpx |
| Backend | FastAPI, async SQLAlchemy, Pydantic v2, Alembic |
| Database | PostgreSQL |
| Dashboard | Next.js, TypeScript, Tailwind, TanStack Query |
| Deploy | Docker Compose |

---

## Open source

Obsero is open source. Anyone can use it, fork it, and contribute.

- **Issues** — bugs, ideas, and discussion welcome  
- **Pull requests** — fixes and features that move the product forward  
- **Self-host** — run it on your own machines; no account required to start  

Large changes are easier to land if you open an issue first so we can align on direction. Keep PRs focused. Match the existing stack unless there’s a strong reason not to.

---

## License

License will be published in a `LICENSE` file before the first tagged release. Until then, treat the repo as source-available for evaluation and contribution discussion.
