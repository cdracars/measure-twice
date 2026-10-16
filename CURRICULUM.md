# Curriculum

The plan, not a promise. Lessons are written one at a time and the plan
changes based on what learners actually find hard. A lesson is listed as
**ready** only once it exists in `lessons/`.

## The project: Jig

Every lesson builds toward **Jig**, a workshop manager. Its parts were chosen
because each one teaches something:

| Part | What it covers | What it teaches |
| --- | --- | --- |
| Machines | FDM printer first; laser or CNC later | Entities; whether the design stretches when a second kind appears |
| Materials | Filament first (grams, density, length); sheet stock later | Value objects, units as types, rules the data must always obey |
| Jobs | queued → running → done / failed / cancelled; compatibility checks (ABS wants an enclosure, the part must fit the bed) | State machines, domain rules |
| G-code import | Read a sliced file's estimates of filament use and print time | Parsing messy real input; one interface with an adapter per slicer |
| Build Log | Dated entries tied to projects | Storage, search |
| Events | "Job finished" uses up material and writes a log entry | Decoupling the parts of the app |
| Front ends | CLI, then an HTTP API, then a React dashboard | Ports and adapters; frontend architecture |

## Stage 1: Basics + TDD rhythm

All four languages side by side. I write the tests at first; by the end you
write them.

| # | Topic | Workshop problem | Status |
| --- | --- | --- | --- |
| 01 | Functions, floats, red → green → refactor | Filament length ↔ weight | **ready** |
| 02 | `if` and `match`, boundary values, writing your first tests | Is this nozzle temperature right for this material? Does it need an enclosure? | **ready** |
| 03 | Structs and classes, encapsulation, mutation; writing all the tests for a method | A `Spool` that tracks what's left and can't be tampered with | **ready** |
| 04 | Enums; making invalid states impossible to represent | Materials (PLA, PETG, ABS, TPU) and verdicts as types, not strings | **ready** |
| 05 | Errors: exceptions vs errors as values; parsers that accept too much | Parse "12.5 g" and "petg", reject "-5 g", "nan" and "0x10"; a spool that refuses to go negative | **ready** |
| 06 | Collections, loops vs pipelines, "no value"; choosing which cases to test | Totals, per-material grams, and the heaviest job in a print queue | **ready** |
| 07 | Strings, Unicode, `String` vs `&str` | Parse and format a log line like `2026-10-16: replaced nozzle`; shorten text without breaking `°` or `🧵` | **ready** |
| 08 | Files, line endings, tests that touch the file system | Load a Build Log, reporting bad lines by number; append new entries | **ready** |
| 09 | Putting it together: a pure `run` function behind a thin entry point; exit codes, stdout vs stderr; writing every test for a command | A small `jig` command-line tool built from lessons 01–08 | **ready** |

Also introduced in this stage: the testing pyramid (why most tests should be
small and fast).

## Stage 2–4: Architecture track

One evolving Jig codebase, restructured lesson by lesson with the tests green
throughout. Work in **your strongest language**, so attention stays on
structure rather than syntax. Every lesson has reference solutions in all four
languages, and a neutral comparison table of how each expresses the same
design. Seeing one architecture in four languages shows which parts are the
design and which are just the language.

| # | Lesson | Idea |
| --- | --- | --- |
| A1 | One messy file, on purpose | Feel why structure matters |
| A2 | Cohesion and coupling | Things that change together live together |
| A3 | Layered architecture | Presentation → domain → data, and the anemic domain model trap |
| A4 | MVC | Familiar from PHP frameworks; maps onto React |
| A5 | Pure core, side effects at the edges | Calculations with no I/O are easy to test |
| A6 | Dependency inversion → ports and adapters | The domain defines interfaces; storage plugs in. Clean and onion architecture are close relatives. |
| A7 | Domain-driven design: bounded contexts | Jobs, inventory, and build log each get their own vocabulary |
| A8 | Domain events, inside one program | "Job finished" triggers inventory and log updates without a queue |
| A9 | Modular monolith vs services | When splitting pays off, and why usually not yet |
| A10 | Tests that enforce the architecture | CI fails if the domain imports storage code |
| A11 | Frontend architecture | The same dashboard two ways: a React app (TypeScript) and server-rendered HTML (PHP, Python, Rust). Where state lives, component vs template boundaries, and what each approach costs |

Woven into these lessons: refactoring, test doubles (fakes and mocks),
value objects, state machines, property-based testing, error-handling
strategy, database migrations (SQLite), configuration and logging.

## Stage 5: Working with AI-written code

- Reading unfamiliar code
- Debugging methodically
- Git workflow and code review
- Reviewing AI output: each exercise gives a plausible solution with a subtle
  bug and weak tests; find both
- Mutation testing: break the code on purpose and see whether the tests
  notice

## Later stages (not planned in detail)

Security basics, SQL beyond the basics, performance and profiling.

Left out on purpose: microservices, event sourcing/CQRS, message queues,
Kubernetes. They solve problems of large teams and heavy traffic.

## How the repo itself is run

You learn these by working inside them, not by reading about them:

- CI on every push: formatting, linting, and type checks everywhere; tests on
  every branch except `main` ([ADR 0002](docs/adr/0002-solutions-on-a-branch.md))
- Built-in tools only in stage 1 ([ADR 0001](docs/adr/0001-built-in-tools-only.md));
  realistic, small frameworks from stage 2 on
  ([ADR 0003](docs/adr/0003-realistic-tools-from-stage-2.md))
- Decisions recorded as ADRs in `docs/adr/`
- Shared vocabulary in [GLOSSARY.md](GLOSSARY.md)
- Later: conventional commits, a dev container, pre-commit hooks

## Reading

- *The Rust Programming Language* (the official book): <https://doc.rust-lang.org/book/>
- Martin Fowler's writing on refactoring and architecture: <https://martinfowler.com/>,
  and his book's site, <https://refactoring.com/>
- Alistair Cockburn, "Hexagonal Architecture" (the original ports-and-adapters
  article): <https://alistair.cockburn.us/hexagonal-architecture/>
- Gary Bernhardt, *Boundaries* (talk, RubyConf 2012), on keeping a functional
  core behind an imperative shell: <https://www.destroyallsoftware.com/talks/boundaries>
- Scott Wlaschin, *Domain Modeling Made Functional* (Pragmatic Bookshelf, 2018;
  examples in F#, ideas that carry straight over to Rust and TypeScript):
  <https://pragprog.com/titles/swdddf/domain-modeling-made-functional/>
- Michael Nygard, "Documenting Architecture Decisions" (2011, the blog post that
  introduced ADRs): <https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions>

Links checked 2026-10-16.
