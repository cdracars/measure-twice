# 5. A dev container for zero-install setup

Date: 2026-10-16

## Status

Accepted. [ADR 0006](0006-a-guide-panel-in-vs-code.md) adds the guide panel,
installed by `post-create.sh`, and replaces the first-terminal hook that
started the guide.

## Context

The course needs four toolchains, and stage 2 adds Composer, uv, and PHP
8.4.1+. Installing all of that is where many learners give up before writing
a line of code. It's also where setups drift: an old Node, a PHP without
`mbstring`, a missing `cargo`.

## Decision

Add `.devcontainer/`, so the repository opens ready to use in GitHub
Codespaces, or locally with VS Code's Dev Containers extension.

- Base image: `mcr.microsoft.com/devcontainers/php:4-8.4-trixie`, Microsoft's
  prebuilt dev container image on the official PHP 8.4 image. It includes
  `mbstring` and the XML extensions PHPUnit needs, and Composer. Prebuilt means
  no compiling PHP on first start.
- Python: Debian trixie's own Python 3.13, through the Python feature's
  `os-provided` option, so nothing is compiled.
- Node.js 22 and Rust stable through the official dev container features.
- uv through Astral's official installer, in `.devcontainer/post-create.sh`,
  which also installs Node packages and builds the Rust lessons once so the
  first test run is quick.
- `XDEBUG_MODE=off`: the base image enables Xdebug for every request, which
  slows every PHP test run and prints connection warnings.

Installing on your own machine stays fully supported; the README offers both.

## Consequences

- One click from the README to a working course, at the cost of Codespaces
  hours (GitHub's free plan includes some each month).
- The first start takes a few minutes while features install; later starts
  are fast.
- The image and feature tags float within their major versions (`4-8.4`,
  `:1`, `:2`), so the container picks up fixes but can change underneath the
  course. If a start breaks, pin exact versions.
- This configuration can't be tested in CI without Docker; it was checked for
  valid JSON, existing image and feature tags, and a working post-create
  script, and needs a real Codespace start to confirm.
