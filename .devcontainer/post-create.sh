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

# The first terminal in Codespaces and VS Code shows this notice.
notice=/usr/local/etc/vscode-dev-containers/first-run-notice.txt
if sudo -n true 2>/dev/null; then
  sudo mkdir -p "$(dirname "$notice")"
  sudo tee "$notice" > /dev/null <<'TEXT'
Welcome to Measure Twice. Everything is installed.

Start the guide:     ./scripts/guide
Or read the course:  README.md

TEXT
fi

echo
echo "Ready. Open a terminal and run: ./scripts/guide"
