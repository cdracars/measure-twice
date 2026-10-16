# 3. Realistic tools from stage 2 on

Date: 2026-10-16

## Status

Accepted. Narrows [ADR 0001](0001-built-in-tools-only.md) to stage 1.
Amended the same day, before any stage 2 lesson existed: FastAPI replaces
Flask.

## Context

ADR 0001 keeps lessons to built-in tools so setup is four installs and the
language is visible without a framework in the way. That suits stage 1.

From stage 2, the course teaches design and architecture, and the goal is
realistic practice. Real projects use test frameworks, package managers, web
frameworks, and database drivers. Part of architecture is keeping a framework
at the edge of your code instead of letting it shape everything. Learners
can't practise that without a framework.

Large frameworks (Laravel, Django, Next.js) are realistic too, but they make
many architecture decisions for you. This course is about making those
decisions yourself.

## Decision

Stage 1 stays built-in tools only (ADR 0001). From stage 2 on, lessons use
small, widely used tools:

| | PHP | Python | TypeScript | Rust |
| --- | --- | --- | --- | --- |
| Tests | PHPUnit | pytest | Vitest | `cargo test` |
| Packages | Composer | uv | npm | cargo |
| Web | Slim | FastAPI + Jinja2 | React + Vite | axum + askama |
| Database | PDO + SQLite | `sqlite3` (standard library) | better-sqlite3 | rusqlite |

Latest stable versions when this was written, all released in 2026:
PHPUnit 13.4, Slim 4.15, pytest 9.1, FastAPI 0.143, uv 0.13, Vitest 5.0,
Vite 8.3, React 19.3, better-sqlite3 13.0, axum 0.8, askama 0.16,
rusqlite 0.40. Jinja2 3.1.6 (March 2025) and Uvicorn 0.54 (FastAPI's
usual server) come with FastAPI.

- Dependencies are pinned with lockfiles (`composer.lock`, `uv.lock`,
  `package-lock.json`, `Cargo.lock`) and updated deliberately.
- Each tool is introduced in the lesson that first needs it, not installed
  up front.
- Stage 2 opens by moving lesson 01's tests from the hand-rolled helpers to
  the real frameworks, so learners see what a framework adds.

## Consequences

- **PHP 8.4.1+ is required from stage 2** (PHPUnit 13's minimum). Stage 1
  still runs on PHP 8.3.
- Setup grows to four package managers. Each lesson lists what it installs.
- `scripts/check` and CI will need per-stage commands when stage 2 lessons
  land.
- Versions go stale. When a lesson is written, check its tools' current
  versions and record changes here or in a new ADR.
- maud was considered for Rust templates. It was not chosen because it had
  no release since February 2025; askama is more actively released.
- Jinja2's latest release is also from 2025. It is kept anyway: it is the
  standard Python template engine, maintained by the Pallets project, and
  mature enough that infrequent releases are expected. Release dates are one
  signal, not the rule.
- FastAPI was chosen over Flask for its type-driven request validation
  (Pydantic), which pairs with the course's focus on types and modeling. It
  also raises an architecture question worth a lesson: Pydantic models are
  convenient, but they belong at the HTTP edge, not in the domain.
