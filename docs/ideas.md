# Ideas

Parked ideas: not plans, not decided, and not part of the curriculum. They're
written down so they aren't lost. The current focus is a stable guide and
onboarding; an idea moves into `CURRICULUM.md` or an ADR only once it's
decided.

- **Go as a fifth language.** `go test` is built in, so it fits stage 1
  (ADR 0001), and `go test -json` is easy for the guide to read. Name tests
  as subtests (`t.Run("zero length weighs nothing", ...)`) so the guide's
  phrases match. Go adds new contrasts: no real enums (04), errors as values
  that nothing forces you to check (05), strings as bytes (07), interfaces
  satisfied implicitly (A6). Cost: Go content for every lesson, a weaker
  "built-in to framework" story for lesson 10, and a fifth comparison column.
  First step if pursued: port lesson 01, and 05 or 07, on a branch to measure
  the real cost per lesson.
- **Only the learner's languages in the dev container.** Install only the
  toolchains a learner chose, for faster starts. (The editor side is done:
  the guide hides other languages' lesson folders in VS Code.) A codespace's
  features are fixed when it's created, so the options are:
  - One configuration per language, at `.devcontainer/<name>/devcontainer.json`
    (Codespaces allows exactly one level below `.devcontainer`). Learners
    pick one in the creation page's dropdown, or from a per-language badge:
    GitHub's "Share a deep link" builds a `codespaces.new` link with the
    configuration chosen. Configurations can't inherit from each other, so
    shared settings are duplicated. Learners who want two languages need a
    combined configuration, or the full one.
  - One lean configuration, with the guide installing toolchains on demand
    after `start`. Slower first step per language and needs root in the
    container, but no combinations to maintain.
  - Either way, the base image is PHP's today; a lean configuration would
    need a neutral base such as Debian with features for each language.

Sources for the dev container options (from the October 2026 session notes):

- GitHub Docs, introduction to dev containers (multiple configurations):
  <https://github.com/github/docs/blob/main/content/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers.md>
- GitHub Docs, quick creation of codespaces (deep links):
  <https://github.com/github/docs/blob/main/content/codespaces/setting-up-your-project-for-codespaces/setting-up-your-repository/facilitating-quick-creation-and-resumption-of-codespaces.md>
