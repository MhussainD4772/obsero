# Future work (post–v0 parking lot)

Ideas we hit while building that we **intentionally deferred**.  
Not a sprint backlog — that’s Jira. This is “we thought about it; don’t forget.”

**Habit:** when a future implementation comes up in chat or review, add a short
entry here in the same session. After v0 / v1.0, mine this for tickets.

---

## How to add an entry

```md
### YYYY-MM-DD — short title
- **Came up in:** OB-N / chat / PR
- **Idea:** one or two sentences
- **Why not now:** one sentence
- **Maybe later:** rough shape if known
```

---

## Entries

### 2026-07-28 — Split local vs Docker frontend workflows more cleanly
- **Came up in:** chat (Turbopack `/app/.next` read-only panic)
- **Idea:** Document “use Compose frontend OR local npm, not both on :3000”; maybe a `compose override` that omits frontend for local UI work.
- **Why not now:** Anonymous `/app/.next` volume fixes the immediate cache poison; process docs can wait.
- **Maybe later:** `docker-compose.override.example.yml` + README note.

### 2026-07-28 — Customer-owned pricing overrides
- **Came up in:** OB-9 (pricing table discussion)
- **Idea:** Let apps pass their own rates, e.g. `obsero.init(pricing={...})`, so models we don’t list still get correct cost.
- **Why not now:** v0 ships a small hardcoded table + FALLBACK; good enough to learn cost_usd end-to-end.
- **Maybe later:** merge user map over defaults; document override shape.

### 2026-07-28 — Backend-owned price table
- **Came up in:** OB-9
- **Idea:** Store $/token rates in Postgres (or config service); SDKs fetch/cache instead of shipping a stale dict.
- **Why not now:** Extra network + cache invalidation before batching/fail-safe exist.
- **Maybe later:** `GET /pricing` + SDK cache TTL; admin update without SDK release.

### 2026-07-28 — Unknown model → null cost (honest) instead of FALLBACK $
- **Came up in:** OB-9
- **Idea:** If model isn’t in the table, leave `cost_usd` null and flag it in UI (“unknown pricing”) rather than a guessed FALLBACK rate.
- **Why not now:** FALLBACK keeps dashboards non-empty while learning; honesty can wait.
- **Maybe later:** `pricing_status: known | fallback | unknown` on the event.

### 2026-07-28 — Durable event buffer (survive process death)
- **Came up in:** OB-9 (batching tradeoff)
- **Idea:** If the process dies mid-buffer, in-memory events are lost. Disk / SQLite / queue for at-least-once shipping.
- **Why not now:** In-memory + atexit flush is enough for v0 DoD; durability is a product hardening step.
- **Maybe later:** local spool file or Redis list before HTTP flush.

### 2026-07-27 — Thin `@obsero.trace` decorator
- **Came up in:** ADR 0002
- **Idea:** Optional decorator that wraps the same context manager for one-liner call sites.
- **Why not now:** Context manager is the chosen API; decorator is sugar.
- **Maybe later:** thin wrapper only — no second instrumentation path.

### 2026-07-28 — Optional provider extras (don’t hard-require google-genai)
- **Came up in:** OB-8 SDK packaging
- **Idea:** Keep core SDK = httpx only; `pip install obsero[gemini]` / `[openai]` for examples.
- **Why not now:** Example path needed google-genai on the package for DoD; fine for learning.
- **Maybe later:** extras in `pyproject.toml`; core stays lean for customers who never call Gemini from the SDK package.
