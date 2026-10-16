# 1. Built-in tools only

Date: 2026-10-16

## Status

Accepted

## Context

Learners need four toolchains: PHP, Python, Node.js, and Rust. Each language
also has popular test frameworks (PHPUnit, pytest, Vitest) and package
managers. Every extra tool is another install step that can fail before the
learner writes a line of code, and another layer of "magic" between them and
the language.

## Decision

Lessons use only what ships with each language:

- PHP: plain scripts with a small `assert_close` helper and `php -l`
- Python: `unittest` from the standard library
- TypeScript: Node's built-in `node:test` runner and type stripping (Node
  22.18+ runs `.ts` files directly)
- Rust: `cargo test`, `rustfmt`, `clippy`

Two development-only exceptions, used for checking code rather than running
lessons:

- `typescript` (and `@types/node`), so `tsc` can check types. Node strips
  types without checking them.
- `ruff`, the Python linter and formatter. CI runs it with `pipx`; learners
  can skip it.

## Consequences

- Setup is four installs and `git clone`.
- Tests read as plain code, with no framework conventions to learn first.
- Learners don't practise the frameworks real projects use. A later lesson can
  introduce them, recorded in a new ADR.
