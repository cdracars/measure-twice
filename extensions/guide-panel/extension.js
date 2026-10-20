// The Measure Twice guide panel. scripts/guide.py stays in charge: it writes its
// current step to .guide-state.json, and this panel shows it. The panel's
// buttons type the same keys into the guide's terminal that a learner would,
// so the terminal and the panel never disagree. See docs/adr/0006.

"use strict";

const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const vscode = require("vscode");
const { render, LANGUAGES } = require("./render");

const TERMINAL_NAME = "Measure Twice guide";
const LANGUAGE_IDS = LANGUAGES.map(([id]) => id);

function readText(file) {
  try {
    return fs.readFileSync(file, "utf8");
  } catch {
    return "";
  }
}

function shellQuote(text) {
  return `'${String(text).replace(/'/g, "'\\''")}'`;
}

function readState(statePath) {
  try {
    return JSON.parse(fs.readFileSync(statePath, "utf8"));
  } catch {
    return null;
  }
}

// The guide keeps the learner's languages in .guide-progress.json.
function languagesChosen(root) {
  const progress = readState(path.join(root, ".guide-progress.json"));
  return Boolean(progress && Array.isArray(progress.languages) && progress.languages.length);
}

// Only the four course languages, each once, in the order the learner clicked.
function validLanguages(text) {
  const picked = String(text).split(/\s+/).filter(Boolean);
  const unique = [...new Set(picked)];
  if (!unique.length || unique.length !== picked.length) return null;
  return unique.every((id) => LANGUAGE_IDS.includes(id)) ? unique : null;
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

// The terminal the panel started the guide in before, still open after the
// guide quit or the window reloaded. Starting again reuses it, so the learner
// doesn't collect a new terminal on every start.
function namedGuideTerminal() {
  return vscode.window.terminals.find((terminal) => terminal.name === TERMINAL_NAME);
}

// Restored terminals open without their names, which arrive a moment later,
// so poll for the name instead of listening for new terminals.
async function guideTerminalRestored(timeout) {
  for (let waited = 0; waited < timeout && !namedGuideTerminal(); waited += 250) {
    await new Promise((resolve) => setTimeout(resolve, 250));
  }
}

class GuidePanel {
  constructor(root) {
    this.root = root;
    this.statePath = path.join(root, ".guide-state.json");
    this.view = undefined;
    this.starting = undefined;
  }

  // Starts the guide and says so in the panel until the guide writes its first
  // state. `reveal` also brings its terminal to the front: for a click, not
  // for the automatic start when the course opens.
  async start(languages, { reveal = false } = {}) {
    if (!(await startGuide(this.root, languages, { reveal }))) return;
    clearTimeout(this.starting && this.starting.timer);
    // If the guide never writes anything (its command was lost, say), offer
    // Start again rather than waiting forever.
    const timer = setTimeout(() => {
      this.starting = undefined;
      this.refresh();
    }, 30000);
    this.starting = { from: readText(this.statePath), timer };
    this.refresh();
  }

  state() {
    const state = readState(this.statePath);
    const live = state && !["stopped", "all-done"].includes(state.status);
    if (live && !guideIsAlive(state)) return { version: 1, status: "stopped" };
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
    if (this.starting && readText(this.statePath) !== this.starting.from) {
      clearTimeout(this.starting.timer);
      this.starting = undefined;
    }
    if (this.view) {
      const html = render(this.state(), {
        trusted: vscode.workspace.isTrusted,
        needsLanguages: !languagesChosen(this.root),
        starting: Boolean(this.starting),
      });
      this.view.webview.postMessage({ type: "render", html });
    }
  }

  async handle({ action, value }) {
    if (action === "trust") {
      await vscode.commands.executeCommand("workbench.trust.manage");
    } else if (action === "choose") {
      const languages = validLanguages(value);
      if (languages) await this.start(languages, { reveal: true });
    } else if (action === "open") {
      await vscode.commands.executeCommand("vscode.open", vscode.Uri.file(path.join(this.root, value)));
    } else if (action === "start") {
      await this.start(undefined, { reveal: true });
    } else if (action === "terminal" || action === "key") {
      // Keys only go to a running guide; "show the terminal" also works while
      // it's still starting.
      const terminal =
        (await findGuideTerminal(this.state())) || (action === "terminal" ? namedGuideTerminal() : undefined);
      if (!terminal) {
        const choice = await vscode.window.showWarningMessage(
          "The panel can't find the terminal the guide is running in.",
          "Start the guide",
        );
        if (choice) await this.start(undefined, { reveal: true });
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
  .tests li { margin: 0.4em 0; }
  .message { font-family: var(--vscode-editor-font-family); font-size: 0.92em; color: var(--vscode-descriptionForeground); margin-left: 1.2em; }
  .hint { padding: 6px 10px; border-radius: 4px; background: var(--vscode-textBlockQuote-background); }
  .how { margin-top: 1.4em; font-size: 0.92em; }
  .picker button, button.secondary { color: var(--vscode-button-secondaryForeground); background: var(--vscode-button-secondaryBackground); }
  .picker button.on { color: var(--vscode-button-foreground); background: var(--vscode-button-background); }
  button:disabled { opacity: 0.5; cursor: default; }
  ol#picked { padding-left: 1.4em; margin: 0.4em 0; }
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
  // The language picker: clicking adds a language to the end of the list (or
  // takes it out), so the order is strongest first.
  let picked = [];
  function showPicked() {
    const list = document.getElementById("picked");
    const start = document.getElementById("choose");
    if (!list || !start) return;
    list.innerHTML = "";
    picked.forEach((id) => {
      const item = document.createElement("li");
      item.textContent = document.querySelector('[data-pick="' + id + '"]').textContent;
      list.appendChild(item);
    });
    document.getElementById("picked-empty").hidden = picked.length > 0;
    document.querySelectorAll("[data-pick]").forEach((b) => b.classList.toggle("on", picked.includes(b.dataset.pick)));
    start.disabled = picked.length === 0;
    start.dataset.value = picked.join(" ");
  }
  app.addEventListener("click", (event) => {
    const pick = event.target.closest("[data-pick]");
    if (pick) {
      const id = pick.dataset.pick;
      picked = picked.includes(id) ? picked.filter((p) => p !== id) : [...picked, id];
      showPicked();
      return;
    }
    if (event.target.closest("[data-pick-reset]")) {
      picked = [];
      showPicked();
      return;
    }
    const button = event.target.closest("button[data-action]");
    if (button && !button.disabled) {
      vscode.postMessage({ action: button.dataset.action, value: button.dataset.value || "" });
    }
  });
</script>
</body>
</html>`;
  }
}

// Starts the guide in a terminal that stays in the background unless `reveal`:
// the panel is what the learner looks at. GUIDE_PANEL=1 tells the guide to keep
// its own screen brief. With `languages`, it first saves them
// (./scripts/guide start). Returns whether it sent the command.
async function startGuide(root, languages, { reveal = false } = {}) {
  if (!languages && !languagesChosen(root)) {
    // Nothing to start yet: the panel shows the language picker.
    vscode.commands.executeCommand("workbench.view.extension.measureTwice");
    return false;
  }
  const state = readState(path.join(root, ".guide-state.json"));
  const running = await findGuideTerminal(state);
  if (running) {
    if (!languages) running.show();
    return false;
  }
  // A guide we can't find a terminal for (another window, say) still counts:
  // the guide itself refuses to run twice, so don't start a second one.
  if (state && !["stopped", "all-done"].includes(state.status) && guideIsAlive(state)) {
    vscode.window.showInformationMessage("The guide is already running in another terminal.");
    return false;
  }
  let command = languages
    ? `./scripts/guide start ${languages.join(" ")} && ./scripts/guide`
    : "./scripts/guide";
  let terminal = namedGuideTerminal();
  if (terminal) {
    // The learner may have moved this terminal away from the course folder.
    command = `cd ${shellQuote(root)} && ${command}`;
  } else {
    terminal = vscode.window.createTerminal({
      name: TERMINAL_NAME,
      cwd: root,
      env: { GUIDE_PANEL: "1" },
    });
  }
  terminal.sendText(command, true);
  if (reveal) terminal.show(true);
  return true;
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
    vscode.commands.registerCommand("measureTwice.startGuide", () => panel.start(undefined, { reveal: true })),
    vscode.window.onDidCloseTerminal(() => panel.refresh()),
    vscode.workspace.onDidGrantWorkspaceTrust(() => panel.refresh()),
  );

  // Polling is simple and works the same in Codespaces, dev containers and locally.
  const progressPath = path.join(root, ".guide-progress.json");
  for (const file of [panel.statePath, progressPath]) {
    fs.watchFile(file, { interval: 500 }, () => panel.refresh());
    context.subscriptions.push({ dispose: () => fs.unwatchFile(file) });
  }

  // Show the panel the first time the course opens; after that, leave the
  // sidebar where the learner put it.
  if (!context.workspaceState.get("measureTwice.shown")) {
    context.workspaceState.update("measureTwice.shown", true);
    vscode.commands.executeCommand("workbench.view.extension.measureTwice");
  }

  // Start the guide when the course opens, so a learner lands on step 1 without
  // typing anything. In Restricted Mode terminals are blocked, so wait for trust.
  // Only on opening: if the learner quits the guide later, the panel offers a
  // Start button instead of restarting it behind their back.
  const autoStart = async () => {
    const state = panel.state();
    if (state && state.status !== "stopped") return;
    // The guide has run here before, so this may be a reload: VS Code brings
    // the old terminals back a few seconds after the panel starts. Wait for
    // the guide's, so starting reuses it instead of opening another.
    if (state) await guideTerminalRestored(8000);
    panel.start();
  };
  if (vscode.workspace.isTrusted) {
    autoStart();
  } else {
    context.subscriptions.push(vscode.workspace.onDidGrantWorkspaceTrust(autoStart));
  }
}

function deactivate() {}

module.exports = { activate, deactivate };
