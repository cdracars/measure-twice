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

# The guide panel: a small VS Code extension in extensions/guide-panel that shows
# the guide's current step in the sidebar (ADR 0006). It isn't on the
# marketplace, so copy it straight into the folders VS Code loads extensions
# from: ~/.vscode-remote in Codespaces, ~/.vscode-server in local dev containers.
echo "Installing the guide panel..."
panel_id="$(node -p "const p = require('./extensions/guide-panel/package.json'); p.publisher + '.' + p.name + '-' + p.version")"
for dir in ~/.vscode-remote/extensions ~/.vscode-server/extensions; do
  mkdir -p "$dir"
  rm -rf "${dir:?}/$panel_id"
  cp -r extensions/guide-panel "$dir/$panel_id"
done

# The first terminal in Codespaces and VS Code shows this notice.
notice=/usr/local/etc/vscode-dev-containers/first-run-notice.txt
if sudo -n true 2>/dev/null; then
  sudo mkdir -p "$(dirname "$notice")"
  sudo tee "$notice" > /dev/null <<'TEXT'
Welcome to Measure Twice. Everything is installed.

The Measure Twice panel in the sidebar takes you through each step.
The guide behind it runs in the "Measure Twice guide" terminal.
Prefer the terminal? Run: ./scripts/guide
Or read the course:      README.md

TEXT
fi

echo
echo "Ready. Open a terminal and run: ./scripts/guide"
