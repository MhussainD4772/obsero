# Architecture Decision Records (ADRs)

ADRs are short notes for **technical decisions that have alternatives**.

## When to write one

Write an ADR when you pick something that would be hard to reverse or that someone else (or future you) would ask "why this way?"

Examples: Postgres vs SQLite, BackgroundTasks vs Redis worker, how auth works, monorepo layout.

Skip ADRs for tiny stuff (variable names, one-off refactors).

## How to use

1. Copy `0000-template.md` → `0002-short-slug.md` (next number)
2. Fill Context → Decision → Alternatives → Consequences
3. Set Status to Accepted when you commit to it
4. If you reverse it later, mark the old one Superseded and link the new ADR

Keep them short. The point is the reasoning, not a essay.
