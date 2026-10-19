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

**Update 2026-10-19:** `guide-panel` (ADR 0006) and then this branch were
merged into `main`, and `main` into `solutions`. The panel shows the same
stable test list as the terminal. The rest of this section is as of the
session's end, before those merges.

- `54c9621` (open the lesson README and stub per step) is on `main`, merged
  as `4354eee` with Cody's follow-up `c09eb2b` (`GUIDE_NO_OPEN=0` leaves
  opening on). Cody's billing note is on `main` too (`edf4af5`).
- The rest is in a pull request from **`guide-open-lesson-files`**, with
  `main` merged in:
  - `726c9a0` Keep a step's tests in a stable list, so a fixed test turns
    green in place
  - `f3bbaf9` Note two ideas under consideration: Go, and only the learner's
    languages
  - `7806d99` Show only the chosen languages' lesson folders in VS Code's
    Explorer
  - `84323d0` Add these notes; `106b5e3` point AGENTS.md at `docs/notes/`
- Verified after merging `main`: 77 guide unit tests pass; `verify
  --structure` passes; ruff check and format pass.
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

### Parked ideas

Go as a fifth language, and dev containers that install only the learner's
languages, were discussed in this session. On 2026-10-19 Cody parked both as
too experimental: the aim for now is a stable guide and onboarding. They're
kept out of the repo, including CURRICULUM.md, until he decides otherwise.

### Possible next steps

- Try the branch in a Codespace and work through "To check".
- Merge or open a PR for `guide-open-lesson-files`, after Cody's billing-note
  commit is pushed.
- Possibly mention the new behaviour in ADR 0004 and 0005 (not done).

### Sources

- GitHub Docs, automatically opening files in codespaces:
  https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/configuring-dev-containers/automatically-opening-files-in-the-codespaces-for-a-repository
- GitHub Docs, introduction to dev containers (multiple configurations):
  https://github.com/github/docs/blob/main/content/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers.md
- GitHub Docs, quick creation of codespaces (deep links):
  https://github.com/github/docs/blob/main/content/codespaces/setting-up-your-project-for-codespaces/setting-up-your-repository/facilitating-quick-creation-and-resumption-of-codespaces.md
- gh codespace create (`--devcontainer-path`):
  https://cli.github.com/manual/gh_codespace_create
