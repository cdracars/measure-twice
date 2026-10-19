#!/usr/bin/env bash
# Runs once, when the dev container is created. Everything the course needs is
# installed by devcontainer.json; this adds uv and warms the caches so the
# first run of the guide is quick.
set -euo pipefail

echo "Installing uv (Python packages for stage 2)..."
curl -LsSf https://astral.sh/uv/install.sh | sh

echo "Installing Node packages (TypeScript checker, Vitest)..."
npm ci --no-audit --no-fund

echo "Building the Rust lessons once, so the first test run is fast..."
cargo test --workspace --no-run --quiet

# In a codespace, the first terminal of each session starts the guide, so a
# learner lands on step 1 without typing anything. Later terminals are plain
# shells. boot_id changes whenever the codespace restarts.
if ! grep -q 'measure-twice-guide' ~/.bashrc 2>/dev/null; then
  cat >> ~/.bashrc <<'BASHRC'

# measure-twice-guide: start the guide in the first terminal of a codespace.
if [ -n "${CODESPACES:-}" ] && [[ $- == *i* ]] && [ -f lessons/01-filament-math/guide.toml ]; then
  _guide_marker="/tmp/measure-twice-guide-$(cat /proc/sys/kernel/random/boot_id 2>/dev/null)"
  if [ ! -e "$_guide_marker" ]; then
    touch "$_guide_marker"
    ./scripts/guide
  fi
  unset _guide_marker
fi
BASHRC
fi

# The first terminal in Codespaces and VS Code shows this notice.
notice=/usr/local/etc/vscode-dev-containers/first-run-notice.txt
if sudo -n true 2>/dev/null; then
  sudo mkdir -p "$(dirname "$notice")"
  sudo tee "$notice" > /dev/null <<'TEXT'
Welcome to Measure Twice. Everything is installed.

The guide starts by itself in this terminal.
Quit it? Start it again: ./scripts/guide
Or read the course:      README.md

TEXT
fi

echo
echo "Ready. Open a terminal and run: ./scripts/guide"
