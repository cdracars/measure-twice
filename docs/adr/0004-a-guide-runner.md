# 4. A guide runner in Python's standard library

Date: 2026-10-16

## Status

Accepted

## Context

The course started as a repository to read through: a lesson README, a stub,
and `scripts/check`. Learners had to work out what to do next themselves, and
the jump from a bare test failure to the `solutions` branch was large. The
target learner leans on AI and gets stuck easily, which is exactly when an
unguided repository loses them.

Tools such as Rustlings show that a runner that watches your files and moves
you through small exercises makes a course much easier to stay with.

## Decision

Add `scripts/guide`, a terminal program that:

- breaks each lesson into steps, defined in `lessons/*/guide.toml`;
- re-runs the current step's tests whenever a file is saved, and shows only
  that step's failures: name, expected vs got, and location;
- gives three hints per step, from a nudge to nearly the answer, in the
  learner's language;
- for test-first steps, only counts the step once it has seen the learner's
  new tests fail;
- keeps progress in `.guide-progress.json`, which git ignores.

It's written in Python's standard library only. Every learner already has
Python for the course, so the guide needs no install, which keeps ADR 0001's
promise for stage 1. Steps find their tests by phrases matched against test
names, so the existing test files didn't need restructuring.

## Consequences

- `scripts/check` stays as the plain, unguided way to run tests.
- Lesson authors maintain `guide.toml` alongside each lesson. CI runs
  `./scripts/guide verify --structure` on every branch (each step's phrases
  match real tests in every language) and `./scripts/guide verify` off `main`
  (every step passes with the reference solutions).
- The guide parses each test runner's output, so a change in a runner's
  output format can break it. Its unit tests use captured real output to make
  that visible.
- Reading keys while watching uses `select()` on standard input, which works
  on macOS, Linux and WSL. On native Windows Python, the watch mode can't read
  keys; the `hint`, `done` and `status` commands work everywhere.
