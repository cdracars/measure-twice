// The Measure Twice guide panel. scripts/guide.py stays in charge: it writes its
// current step to .guide-state.json, and this panel shows it. The panel's
// buttons type the same keys into the guide's terminal that a learner would,
// so the terminal and the panel never disagree. See docs/adr/0006.

"use strict";

const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const vscode = require("vscode");
const { render } = require("./render");

const TERMINAL_NAME = "Measure Twice guide";

function readState(statePath) {
  try {
    return JSON.parse(fs.readFileSync(statePath, "utf8"));
  } catch {
    return null;
  }
}

// The guide lists its own process first. If that process is gone (the terminal
// was closed, or the guide crashed), the state on disk is stale.
function guideIsAlive(state) {
  if (!state || !Array.isArray(state.pids) || !state.pids.length) return false;
  try {
    process.kill(state.pids[0], 0);
    return true;
  } catch (error) {
    return error.code === "EPERM";
  }
}

async function findGuideTerminal(state) {
  if (!state || !Array.isArray(state.pids)) return undefined;
  for (const terminal of vscode.window.terminals) {
    const pid = await terminal.processId;
    if (pid && state.pids.includes(pid)) return terminal;
  }
  return undefined;
}

class GuidePanel {
  constructor(root) {
    this.root = root;
    this.statePath = path.join(root, ".guide-state.json");
    this.view = undefined;
  }

  state() {
    const state = readState(this.statePath);
    if (state && state.step && !guideIsAlive(state)) return { version: 1, status: "stopped" };
    return state;
  }

  resolveWebviewView(view) {
    this.view = view;
    view.webview.options = { enableScripts: true };
    view.webview.html = this.page(view.webview);
    view.webview.onDidReceiveMessage((message) => this.handle(message));
    view.onDidChangeVisibility(() => view.visible && this.refresh());
    this.refresh();
  }

  refresh() {
    if (this.view) {
      const html = render(this.state(), { trusted: vscode.workspace.isTrusted });
      this.view.webview.postMessage({ type: "render", html });
    }
  }

  async handle({ action, value }) {
    if (action === "trust") {
      await vscode.commands.executeCommand("workbench.trust.manage");
    } else if (action === "open") {
      await vscode.commands.executeCommand("vscode.open", vscode.Uri.file(path.join(this.root, value)));
    } else if (action === "start") {
      await startGuide(this.root);
    } else if (action === "terminal" || action === "key") {
      const terminal = await findGuideTerminal(this.state());
      if (!terminal) {
        const choice = await vscode.window.showWarningMessage(
          "The panel can't find the terminal the guide is running in.",
          "Start the guide",
        );
        if (choice) await startGuide(this.root);
        return;
      }
      if (action === "key") terminal.sendText(value, true);
      if (action === "terminal" || value === "o") terminal.show();
    }
  }

  page(webview) {
    const nonce = crypto.randomBytes(16).toString("base64");
    return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'nonce-${nonce}';">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body { color: var(--vscode-foreground); font-family: var(--vscode-font-family); font-size: var(--vscode-font-size); line-height: 1.5; padding: 0 12px 16px; }
  h2 { font-size: 1.15em; margin: 0.6em 0 0.4em; }
  h3 { font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.04em; color: var(--vscode-descriptionForeground); margin: 1.4em 0 0.4em; }
  p { margin: 0.5em 0; }
  code { font-family: var(--vscode-editor-font-family); }
  .muted { color: var(--vscode-descriptionForeground); }
  .good { color: var(--vscode-testing-iconPassed); }
  .bad { color: var(--vscode-testing-iconFailed); }
  .quiet { color: var(--vscode-descriptionForeground); }
  .bar { height: 4px; background: var(--vscode-editorWidget-border, rgba(128,128,128,0.3)); border-radius: 2px; }
  .bar div { height: 100%; background: var(--vscode-progressBar-background); border-radius: 2px; }
  .intro { border-left: 3px solid var(--vscode-textLink-foreground); padding: 2px 10px; margin: 0.8em 0; background: var(--vscode-textBlockQuote-background); }
  .next { font-weight: 600; padding: 8px 10px; border-radius: 4px; background: var(--vscode-textBlockQuote-background); }
  .row { display: flex; flex-wrap: wrap; gap: 6px; margin: 0.6em 0; }
  button { font: inherit; color: var(--vscode-button-foreground); background: var(--vscode-button-background); border: none; border-radius: 3px; padding: 4px 10px; cursor: pointer; }
  button:hover { background: var(--vscode-button-hoverBackground); }
  .row button[data-action="open"], .footer button { color: var(--vscode-button-secondaryForeground); background: var(--vscode-button-secondaryBackground); }
  .row button[data-action="open"]:hover, .footer button:hover { background: var(--vscode-button-secondaryHoverBackground); }
  ul { padding-left: 0; list-style: none; margin: 0.4em 0; }
  .checklist li { margin: 0.35em 0; }
  .checklist label { display: flex; gap: 6px; align-items: flex-start; }
  .checklist input { margin-top: 0.3em; }
  .failures li { margin: 0.4em 0; }
  .message { font-family: var(--vscode-editor-font-family); font-size: 0.92em; color: var(--vscode-descriptionForeground); margin-left: 1.2em; }
  .hint { padding: 6px 10px; border-radius: 4px; background: var(--vscode-textBlockQuote-background); }
  .how { margin-top: 1.4em; font-size: 0.92em; }
</style>
</head>
<body>
<div id="app"><p class="muted">Loading the guide…</p></div>
<script nonce="${nonce}">
  const vscode = acquireVsCodeApi();
  const app = document.getElementById("app");
  let checks = vscode.getState() || {};
  let stepKey = "";
  window.addEventListener("message", (event) => {
    if (event.data.type !== "render") return;
    app.innerHTML = event.data.html;
    const heading = app.querySelector("h2");
    stepKey = heading ? heading.textContent : "";
    app.querySelectorAll("input[data-check]").forEach((box) => {
      box.checked = Boolean((checks[stepKey] || {})[box.dataset.check]);
    });
  });
  app.addEventListener("change", (event) => {
    const box = event.target.closest("input[data-check]");
    if (!box) return;
    checks[stepKey] = { ...(checks[stepKey] || {}), [box.dataset.check]: box.checked };
    vscode.setState(checks);
  });
  app.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-action]");
    if (button) vscode.postMessage({ action: button.dataset.action, value: button.dataset.value || "" });
  });
</script>
</body>
</html>`;
  }
}

async function startGuide(root) {
  const running = await findGuideTerminal(readState(path.join(root, ".guide-state.json")));
  if (running) {
    running.show();
    return;
  }
  const terminal = vscode.window.createTerminal({ name: TERMINAL_NAME, cwd: root });
  terminal.show();
  terminal.sendText("./scripts/guide", true);
}

function activate(context) {
  const folder = (vscode.workspace.workspaceFolders || []).find((f) =>
    fs.existsSync(path.join(f.uri.fsPath, "scripts", "guide.py")),
  );
  if (!folder) return;
  const root = folder.uri.fsPath;
  const panel = new GuidePanel(root);

  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider("measureTwice.guide", panel, {
      webviewOptions: { retainContextWhenHidden: true },
    }),
    vscode.commands.registerCommand("measureTwice.startGuide", () => startGuide(root)),
    vscode.window.onDidCloseTerminal(() => panel.refresh()),
    vscode.workspace.onDidGrantWorkspaceTrust(() => panel.refresh()),
  );

  // Polling is simple and works the same in Codespaces, dev containers and locally.
  fs.watchFile(panel.statePath, { interval: 500 }, () => panel.refresh());
  context.subscriptions.push({ dispose: () => fs.unwatchFile(panel.statePath) });

  // Show the panel the first time the course opens; after that, leave the
  // sidebar where the learner put it.
  if (!context.workspaceState.get("measureTwice.shown")) {
    context.workspaceState.update("measureTwice.shown", true);
    vscode.commands.executeCommand("workbench.view.extension.measureTwice");
  }
}

function deactivate() {}

module.exports = { activate, deactivate };
