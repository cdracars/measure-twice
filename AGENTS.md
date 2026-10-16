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

## When working on the course itself

- Read `CURRICULUM.md`, `GLOSSARY.md`, and `docs/adr/` first.
- Keep lessons built-in-tools only (ADR 0001).
- New lessons go on `main` as stubs plus tests; implement them on `solutions`
  and keep that branch green (ADR 0002).
- Verify with `./scripts/check` on `solutions`, plus the lint steps in
  `.github/workflows/ci.yml`.
- Use glossary terms in code and lesson text; add new terms when a lesson
  introduces them.
