# 6. A guide panel in VS Code

Date: 2026-10-17

## Status

Accepted

## Context

The guide (ADR 0004) runs in a terminal. Once lessons gained an intro, a
"Next" line, checklists and hints, one terminal pane had to hold all of it,
scrolling past the test failures, and learners moved around by typing a
letter and pressing Enter. Testing the Codespace flow as a newcomer showed
that this is cramped, and that a beginner's first screen in VS Code is busy:
build folders, lockfiles and config files they don't need yet.

A web app of our own would need to run four languages' toolchains for every
learner, which means hosting and paying for that compute. Codespaces already
runs it, on each learner's own account (ADR 0005).

## Decision

Add a small VS Code extension, `extensions/guide-panel`, that shows the
guide's current step in the sidebar: the lesson intro, the task, the Next
line, the checklist, test results, hints, and buttons to open the README,
tests and stub.

- **The guide stays in charge.** `scripts/guide.py` writes the current step to
  `.guide-state.json` (git ignores it) whenever it re-runs the tests or shows a
  hint, and marks it stopped when it exits. The panel only displays that file.
  No guide logic lives in the extension, so the terminal and the panel can't
  disagree.
- **The panel starts the guide.** When the course opens and the folder is
  trusted, the panel starts the guide in a "Measure Twice guide" terminal
  (in Restricted Mode, terminals are blocked, so it explains that and waits
  for trust). This replaces an earlier first-terminal hook in `~/.bashrc`, so
  there is one way to start. The guide itself refuses to run while another
  guide is running, so two can never fight over the progress file.
- **Buttons type keys.** Hint, Done and Full output send the same keys to the
  guide's terminal that a learner would type. The panel finds that terminal
  by matching the process IDs the guide writes into its state.
- **No build step, no dependencies.** Plain JavaScript (CommonJS), so there's
  nothing to compile or bundle. `render.js` turns state into HTML without the
  VS Code API and has `node:test` tests; CI runs them in the lint job.
- **Installed by the dev container.** The extension isn't published to the
  marketplace. `post-create.sh` copies it into the folders VS Code loads
  extensions from (`~/.vscode-remote/extensions` in Codespaces,
  `~/.vscode-server/extensions` in local dev containers).
- **A quieter Explorer.** The dev container's `files.exclude` hides build
  output, caches, lockfiles, config files and setup folders, so a codespace
  opens on `lessons/` and the READMEs. Local clones are unaffected.

## Consequences

- The terminal guide works exactly as before, with or without the panel, and
  in any editor. The panel is an extra view, not a requirement.
- Changes to what a step shows go in `guide.py` (`panel_state`) and, if they
  need new layout, `render.js`. The panel's look follows the learner's VS Code
  theme through its CSS variables.
- Copying an extension into VS Code's folder is less official than installing
  a `.vsix`, and VS Code could change how it scans that folder. If the panel
  stops appearing in a fresh codespace, package it with `vsce` and install the
  `.vsix` from the first-terminal hook instead.
- Like the dev container itself, this can't be tested end to end in CI. The
  guide's state and the panel's rendering are unit-tested; a fresh codespace
  confirms the rest.
