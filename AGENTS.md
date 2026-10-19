# Guidance for AI coding assistants

This is a course. The person you're helping is most likely a learner working
through it, and the point is that **they** write the exercise code.

## When helping a learner with an exercise

- Don't write or complete the body of a lesson stub unless they explicitly ask
  for the answer.
- Help in this order, stopping as soon as they're unstuck:
  1. Ask what they expect to happen and what actually happens.
  2. Explain what the failing test or compiler error is saying.
  3. Point to the concept or documentation involved.
  4. Give a hint: a smaller step, or a related example that isn't the answer.
  5. Only if asked directly: show the solution, then suggest they rewrite it
     from memory.
- Never edit tests to make them pass. Learners may add tests.
- Reference solutions are on the `solutions` branch. Don't read from it
  unless the learner asks you to.
- If the learner uses `./scripts/guide` or the Measure Twice panel in VS Code,
  its hints for the current step are in that lesson's `guide.toml`. Prefer
  pointing them to the next hint (`h` in the guide, "Show a hint" in the
  panel) over writing your own.

## When working on the course itself

- Read `CURRICULUM.md`, `GLOSSARY.md`, and `docs/adr/` first.
- Stage 1 lessons use built-in tools only (ADR 0001). Stage 2 on uses the
  tools listed in ADR 0003; check their current versions when writing a
  lesson.
- New lessons go on `main` as stubs plus tests; implement them on `solutions`
  and keep that branch green (ADR 0002).
- Verify with `./scripts/check` on `solutions`, plus the lint steps in
  `.github/workflows/ci.yml`.
- Guided lessons have a `guide.toml` (ADR 0004). When you change a lesson's
  tests, run `./scripts/guide verify --structure` on `main` and
  `./scripts/guide verify` on `solutions`. The guide's own tests:
  `python3 -m unittest discover -s scripts`.
- The guide panel (`extensions/guide-panel`, ADR 0006) only displays the
  guide's `.guide-state.json`. Change what a step shows in `guide.py`
  (`panel_state`), and its layout in `render.js`. The panel's tests:
  `node --test "extensions/guide-panel/test/*.test.js"`.
- Use glossary terms in code and lesson text; add new terms when a lesson
  introduces them.

## Commit identity

Author and commit only as `Cody Dracars <cdracars@gmail.com>`. Never use a
work or employer email address for commits in this repository.

Before committing, check `git config user.email`. If it shows anything else,
pass the identity for that commit (`git -c user.name="Cody Dracars" -c
user.email=cdracars@gmail.com commit ...`) or set it for this repository only;
don't change global git config. Don't rewrite existing history to change
authors unless Cody asks.
