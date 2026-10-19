# Claude Project setup: Measure Twice — guide and onboarding

Paste section 1 into the project's **instructions**. Save section 2 as a
**knowledge** file (for example `session-2026-10-19.md`).

---

## 1. Project instructions

This project is about Measure Twice (github.com/cdracars/measure-twice), a TDD
course in PHP, Python, TypeScript and Rust, and especially about its learner
tooling: `scripts/guide`, the dev container, and onboarding in Codespaces.

- The repository is the source of truth. The knowledge files are dated
  snapshots of past sessions: check them against the repo before treating
  anything as current.
- Follow the repo's AGENTS.md: learners write the exercise code; never edit
  tests to make them pass; read CURRICULUM.md, GLOSSARY.md and docs/adr/
  before changing the course; stage 1 uses built-in tools only (ADR 0001).
- Commit only as `Cody Dracars <cdracars@gmail.com>`.
- Verify guide changes with `python3 -m unittest discover -s scripts`,
  `./scripts/guide verify --structure` on main, and the lint steps in
  `.github/workflows/ci.yml` (ruff check, ruff format --check, and the rest).
- Distinguish verified facts, inferences, proposals and unknowns. Cody
  decides; Claude suggests.

---

## 2. Knowledge: session of 2026-10-16 to 2026-10-19

### Where things stand

- Branch **`guide-open-lesson-files`**, pushed, **not merged, no PR**. Four
  commits on top of `main`:
  - `54c9621` Open the lesson README and stub when a guided step starts
  - `726c9a0` Keep a step's tests in a stable list, so a fixed test turns
    green in place
  - `f3bbaf9` Note two ideas under consideration: Go, and only the learner's
    languages
  - `7806d99` Show only the chosen languages' lesson folders in VS Code's
    Explorer
- Cody's local `main` had one unpushed commit adding a billing note to the
  README's Codespaces section. This branch's README edits are in "Start with
  the guide", away from that section, so a clean merge is expected (not
  checked).
- Verified on the branch: 58 guide unit tests pass; `verify --structure`
  passes; ruff, PHP syntax, TypeScript typecheck, cargo fmt and clippy pass.
- **Not yet tried in a real Codespace.** See "To check" below.

### What changed and why

1. **Opening the lesson files.** The guide told learners to read the lesson
   README, which was hard to find in the Explorer.
   - When a step starts, if the guide runs in VS Code's terminal
     (`TERM_PROGRAM=vscode`) and `code` is on PATH, it runs
     `code --reuse-window <lesson README> <stub>`. This happens once per step,
     not on every re-run.
   - Elsewhere it prints the paths. The list now starts with `Read …/README.md`.
   - Turned off with `--no-open` or `GUIDE_NO_OPEN=1`.
   - Decision: the `TERM_PROGRAM` check was added beyond the original ask, so
     a plain terminal doesn't launch VS Code windows.
   - New key **`r`** opens the lesson README the same way `e` opens the stub
     (`$VISUAL`/`$EDITOR`, then `code`, then a printed path).
2. **Dev container.**
   - `customizations.codespaces.openFiles` is now `README.md` and
     `lessons/01-filament-math/README.md`. The first file gets focus; this
     only works in the browser version of VS Code.
   - `workbench.editorAssociations` maps `**/lessons/*/README.md` to
     `vscode.markdown.preview.editor`, so lesson READMEs open as a preview.
3. **Stable test list.** Cody saw a fixed test vanish and the failure list
   just move down.
   - The report now shows "N of M passing", then every test in the step: ✓ on
     one line, ✗ with message and location.
   - Order: the step's phrases in `guide.toml`, then name. The runner's own
     order isn't used because `cargo test` prints in completion order.
4. **Only the chosen languages in the Explorer.**
   - On first run and on `./scripts/guide start`, the guide sets
     `files.exclude` in `.vscode/settings.json` for the lesson folders of
     languages not chosen.
   - Entries the learner set to `false` stay. A settings file that isn't
     plain JSON (comments) is left alone.
   - `.vscode/settings.json` is now git-ignored, so `git add -A` won't commit
     it.
   - Decision: it hides languages *not chosen*, not "every language but the
     current one", so learners can still see earlier work for the comparison
     tables. Switching is a few lines if wanted.
   - Side effect: `files.exclude` also hides those folders from search and
     Quick Open.

### To check in a real Codespace

- Does the `**/lessons/*/README.md` editor association match? No source found
  documenting path patterns in that setting. If it doesn't match, the README
  opens as plain text and nothing breaks.
- With two files in one `code` call, which one ends up active? The stub
  (opened last) is expected.
- Does the Explorer update live after the guide writes
  `.vscode/settings.json`?
- Authors editing lesson READMEs in a codespace get the preview first;
  "Reopen Editor With…" switches back.

### Ideas under consideration

Both are also recorded in CURRICULUM.md, "Ideas under consideration".

**Only the learner's languages in the dev container** (Cody's original
intention; the Explorer part above was the easy win). The goal is to install
only the chosen toolchains, for faster starts. From GitHub's docs:
- Extra configurations go at `.devcontainer/<name>/devcontainer.json`,
  exactly one level deep. The codespace creation page lists them in a
  dropdown.
- "Share a deep link" builds a `codespaces.new` link or badge with a
  configuration chosen. The URL parameter's name isn't documented, so copy it
  from that dialog.
- Configurations can't inherit from each other, so shared settings are
  duplicated. Learners wanting two languages need a combined or full
  configuration.
- Alternative: one lean configuration where the guide installs toolchains on
  demand after `start`.
- Either way, today's base image is PHP's; a lean configuration needs a
  neutral base.
- Claude's lean: per-language badges. Not decided.

**Go as a fifth language.**
- Fit: `go test` is built in (fits ADR 0001), and `go test -json` is easy to
  parse.
- Use subtests (`t.Run("zero length weighs nothing", …)`) so the guide's
  phrases match test names.
- New contrasts: no real enums (lesson 04), unchecked errors as values (05),
  strings as bytes (07), implicit interfaces (A6).
- Costs: Go content for all 10 lessons, a weaker story for lesson 10, and a
  fifth comparison column.
- Suggested first step: port lesson 01, plus 05 or 07, on a branch. Go
  versions and the dev container Go feature not yet checked.

### Possible next steps

- Try the branch in a Codespace and work through "To check".
- Merge or open a PR for `guide-open-lesson-files`, after Cody's billing-note
  commit is pushed.
- Possibly mention the new behaviour in ADR 0004 and 0005 (not done).
- Decide on per-language containers; if yes, prototype one language's
  configuration and badge.

### Sources

- GitHub Docs, automatically opening files in codespaces:
  https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/configuring-dev-containers/automatically-opening-files-in-the-codespaces-for-a-repository
- GitHub Docs, introduction to dev containers (multiple configurations):
  https://github.com/github/docs/blob/main/content/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers.md
- GitHub Docs, quick creation of codespaces (deep links):
  https://github.com/github/docs/blob/main/content/codespaces/setting-up-your-project-for-codespaces/setting-up-your-repository/facilitating-quick-creation-and-resumption-of-codespaces.md
- gh codespace create (`--devcontainer-path`):
  https://cli.github.com/manual/gh_codespace_create
