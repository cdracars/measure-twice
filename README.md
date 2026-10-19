# Measure Twice

*Measure twice, cut once: write the test, then the code.*

A hands-on course for programmers who can get software built, often with AI
writing most of it, but want to understand what they're shipping. You'll
practise test-driven development, domain modeling, and software architecture
in **PHP, Python, TypeScript, and Rust** by building **Jig**, a manager for a
maker's workshop: 3D printers and other machines, the jobs running on them,
the materials they use up, and a log of what happened.

**Status:** stage 1 (lessons 01–09) and the stage 2 opener (lesson 10) are
ready; the architecture track grows one lesson at a time. See
[CURRICULUM.md](CURRICULUM.md) for the plan.

## Who it's for

- You can read code and get things working, but you lean on AI or copy-paste
  more than you'd like.
- You know at least one of the four languages reasonably well. The course
  uses the one you know as a reference point for the ones you don't.
- You want the habits that make AI-written code safe to accept: tests first,
  clear models, deliberate structure, and critical review.

No 3D printer needed. Every lesson explains the workshop details it uses.

## How it works

Each lesson is one problem, usually solved in all four languages. Start with
the language you know best, so the problem is clear before the syntax gets
in the way, then do the ones you're learning, with your weakest last. You get a
stub and a set of failing tests.

1. **Red:** run the tests, read why they fail.
2. **Green:** write the simplest code that passes.
3. **Refactor:** make it clean while the tests keep you safe.
4. **Your test:** add a test of your own.

Early lessons give you the tests. Later lessons give you a requirement and
expect you to write the tests yourself. That progression *is* the TDD
lesson.

## Setup

### The quick way: nothing to install

Open the course in a GitHub Codespace: VS Code in your browser with PHP 8.4,
Python, Node.js, Rust, Composer and uv already set up.

> [!NOTE]
> **The first start is slow.** A new codespace installs four languages'
> toolchains before it opens, which takes several minutes. The page may sit on
> "Setting up your codespace" for a while: that's normal, so leave it running.
> Reopening the same codespace later takes seconds.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/cdracars/measure-twice)

VS Code may first ask **"Do you trust the authors of the files in this
folder?"** Choose **Trust Folder & Continue**: the guide runs each lesson's
tests, and VS Code keeps terminals switched off until you do.

Once it opens, the **Measure Twice** panel in the sidebar asks which
languages you'll work in, then takes you through each step: what to do, which
tests pass, and buttons for hints and for opening the files. The guide runs in
a terminal behind it, re-running your tests every time you save.

The codespace runs on your own GitHub account, not the course's: GitHub's
"paid for by" notice will show your username. It comes out of your account's
free monthly Codespaces allowance, and with GitHub's default $0 spending limit
it stops when that runs out rather than charging you. Stop or delete the
codespace when you're done to make the allowance last.

The same setup runs on your own machine with VS Code's Dev Containers
extension and Docker: open the folder, then choose *Reopen in Container*. The
configuration is in `.devcontainer/`.

### On your own machine

Install the four toolchains:

| Language | Install | Check |
| --- | --- | --- |
| PHP 8.3+ | <https://www.php.net/downloads> or your package manager | `php --version` |
| Python 3.12+ | <https://www.python.org/downloads/> | `python3 --version` |
| Node.js 22.18+ (runs TypeScript directly) | <https://nodejs.org/> | `node --version` |
| Rust (stable) | <https://rustup.rs/> | `cargo --version` |

Then:

```sh
git clone https://github.com/cdracars/measure-twice
cd measure-twice
git switch -c my-work          # keep your answers on your own branch
./scripts/check 01 rust        # your strongest language: php, python, ts, or rust
                               # see lesson 01 fail; now make it pass
```

`npm install` is only needed for the TypeScript type checker (`npm run
typecheck`). Running the TypeScript tests needs nothing but Node.

Stage 1 needs only the four languages. From stage 2, lessons use real test and
web frameworks and need PHP 8.4.1+; each lesson lists what to install. See
[ADR 0003](docs/adr/0003-realistic-tools-from-stage-2.md).

On Windows, use WSL or Git Bash: `scripts/check` is a bash script.

## Start with the guide

The easiest way in is the guide, a small program that walks you through the
lessons one step at a time.

In a codespace, or the dev container on your own machine, you use it through
the **Measure Twice** panel in VS Code's sidebar. The panel shows your step,
which tests pass and fail, and buttons for hints, for confirming a checklist,
for the full test output, and for opening the lesson's files. The guide itself
runs in the "Measure Twice guide" terminal behind it; leave that terminal open.

Anywhere else, run the guide in a terminal:

```sh
./scripts/guide
```

The rest of this section is about that terminal version.

The first time, it asks which languages you'll use (strongest first) and
checks they're installed. In VS Code, the Explorer then shows only those
languages' lesson folders; `./scripts/guide start` with a different list
changes that. Then it shows your current step, and every time you
save a file it re-runs that step's tests and shows what failed: expected,
got, and where. When the step passes, it moves you on.

Keep it running in a terminal next to your editor; any editor works. In VS
Code's terminal, including a Codespace, each new step opens the lesson README,
the tests, and the file you edit for you. Elsewhere, the guide prints their paths. To
stop it opening files, run `./scripts/guide --no-open` or set
`GUIDE_NO_OPEN=1`. While it's running, type a letter and press Enter:

| Key | Does |
| --- | --- |
| `h` | Show the next hint. Each step has three, from a nudge to nearly the answer. |
| `e` | Open the file you edit, in `$EDITOR` or VS Code |
| `r` | Open the lesson README, which explains the problem, in `$EDITOR` or VS Code |
| `o` | Show the full test output |
| `d` | Confirm a checklist step, such as a refactor |
| `q` | Quit. Your progress is saved. |

`./scripts/guide status` shows where you are; `./scripts/guide help` lists
the rest. Some steps make you write the tests yourself, and the guide only
counts them once it has seen them fail: that's test-first, enforced.

Lessons 01 and 02 are guided so far. For the others, follow the lesson README
as described below.

## Your first 15 minutes without the guide

This walks through lesson 01 by hand, in one language. Pick the one you know
best; the examples use PHP.

1. **Open the project.** Open the `measure-twice` folder in your editor
   (`code .` for VS Code) and keep a terminal open in the same folder.

2. **Read the lesson.** Open `lessons/01-filament-math/README.md`. It explains
   the problem, gives the formula, and lists the file you edit for each
   language.

3. **Red: watch it fail.**

   ```sh
   ./scripts/check 01 php
   ```

   Every test fails with a `TODO: implement …` message. That's the starting
   point: the tests exist, the code doesn't yet.

4. **Green: make it pass.** Open `lessons/01-filament-math/php/filament.php`,
   replace the `throw` line with your code, and run the check again. Read
   which test still fails and what it expected, change the code, and repeat
   until the summary says `passed: 1`. Read the test file as much as you like,
   but don't change the existing tests: they're the spec.

5. **Refactor.** With everything green, make the code clearer: name the
   in-between values, remove repetition. Re-run the check after each change.

6. **Add a test of your own.** The lesson README suggests one. Work out the
   expected value by hand before you run it.

7. **Save your progress.**

   ```sh
   git add -A
   git commit -m "Lesson 01 in PHP"
   ```

8. **Next language.** Repeat with `./scripts/check 01 python`, `ts`, and
   `rust`, filling in the lesson's comparison table as you go. The first Rust
   run takes a minute while it compiles.

Stuck? Re-read the failing test's message first: it says what was expected
and what came back. After that, ask an AI assistant (see below), or look at
the [`solutions`](../../tree/solutions) branch as a last resort.

If you fork this repository and push your branch, CI runs your tests on
GitHub too.

## Running the tests

```sh
./scripts/check              # every lesson, every language
./scripts/check 01           # one lesson
./scripts/check 01 rust      # one lesson, one language
```

## Solutions

Reference solutions live on the [`solutions`](../../tree/solutions) branch.
Try first. Struggling with a failing test is where the learning happens.

## Using an AI assistant

Go ahead, but make it a tutor, not a ghostwriter. This repo's
[AGENTS.md](AGENTS.md) asks AI coding assistants to give hints before answers
and to explain rather than write your exercise code. If you want the answer,
ask for it explicitly, and then write it again yourself without looking.

## Layout

```text
lessons/NN-name/     one lesson: README.md plus php/ python/ ts/ rust/
scripts/check        test runner
scripts/guide        the guided way through the lessons (lessons/*/guide.toml)
extensions/          the guide panel for VS Code, installed by the dev container
CURRICULUM.md        the stages and what each lesson covers
GLOSSARY.md          workshop and course vocabulary
docs/adr/            decisions about how this course is built, and why
```

## License

[MIT](LICENSE)
