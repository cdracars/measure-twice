# 2. Solutions on a branch

Date: 2026-10-16

## Status

Accepted

## Context

Learners should see stubs and failing tests, not answers. But every test must
be provably passable, or a learner can get stuck on a broken exercise.

## Decision

- `main` holds the course: lesson text, stubs, and tests. Its tests fail on
  purpose.
- The `solutions` branch is `main` with every stub implemented.
- CI runs formatting, linting, and type checks on every branch. It runs the
  tests on every branch **except** `main`, so the `solutions` branch must
  always be green.
- When a lesson is added to `main`, `main` is merged into `solutions` and the
  new stubs are implemented there.

## Consequences

- A learner working on their own branch or fork gets real test results in CI.
- Answers are public but one deliberate step away.
- `solutions` can fall behind `main`. A lesson isn't marked **ready** in
  `CURRICULUM.md` until `solutions` passes it.
