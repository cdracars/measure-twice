// Turns the guide's state (.guide-state.json, written by scripts/guide.py) into
// the panel's HTML. No VS Code API here, so it can be tested with plain Node.

"use strict";

function escape(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// Text from guide.toml is wrapped at ~80 columns; blank lines separate paragraphs.
function paragraphs(text, className = "") {
  const cls = className ? ` class="${className}"` : "";
  return String(text)
    .split(/\n\s*\n/)
    .map((p) => p.replace(/\s*\n\s*/g, " ").trim())
    .filter(Boolean)
    .map((p) => `<p${cls}>${escape(p)}</p>`)
    .join("");
}

function button(label, action, value = "", extra = "") {
  const data = value ? ` data-value="${escape(value)}"` : "";
  return `<button data-action="${action}"${data}${extra}>${escape(label)}</button>`;
}

function notRunning(state) {
  if (state && state.status === "all-done") {
    return (
      `<h2>You've finished every guided step.</h2>` +
      `<p>The later lessons aren't guided yet: continue with their READMEs and ` +
      `<code>./scripts/check</code>.</p>`
    );
  }
  return (
    `<h2>The guide isn't running</h2>` +
    `<p>The guide runs in a terminal and this panel follows it.</p>` +
    button("Start the guide", "start")
  );
}

function results(state) {
  const r = state.results;
  if (state.status === "testing" || !r) {
    return `<p class="muted">Running the tests…</p>`;
  }
  const parts = [];
  // Every test in the step, always in the same order: a fixed test turns
  // green where it was instead of dropping out of the list.
  const tests = r.tests || [];
  if (tests.length) {
    const passing = tests.filter((t) => t.passed).length;
    const allPass = passing === tests.length;
    parts.push(`<p${allPass ? ' class="good"' : ""}>${passing} of ${tests.length} passing</p>`);
    parts.push(
      "<ul class=\"tests\">" +
        tests
          .map((t) =>
            t.passed
              ? `<li><span class="good">✓</span> ${escape(t.name)}</li>`
              : `<li><span class="bad">✗</span> ${escape(t.name)}` +
                (t.message ? `<div class="message">${escape(t.message)}</div>` : "") +
                "</li>",
          )
          .join("") +
        "</ul>",
    );
  }
  if (r.notice) {
    parts.push(`<p class="${escape(r.tone)}">${escape(r.notice)}</p>`);
  }
  return parts.join("");
}

// VS Code's Restricted Mode blocks terminals, so the guide can't run until the
// learner trusts the folder. Say so plainly instead of showing a dead panel.
function untrusted() {
  return (
    `<h2>Trust this folder to start</h2>` +
    `<p>VS Code is asking whether you trust the authors of this folder. The ` +
    `guide runs the lesson's tests, which needs a terminal, so VS Code keeps it ` +
    `switched off until you choose <b>Trust</b>.</p>` +
    `<p class="muted">This is the course repository you opened yourself. Trusting ` +
    `it lets the guide and the tests run.</p>` +
    button("Trust this folder", "trust")
  );
}

const LANGUAGES = [
  ["php", "PHP"],
  ["python", "Python"],
  ["ts", "TypeScript"],
  ["rust", "Rust"],
];

// The first run asks which languages, strongest first. The order matters, so
// the learner clicks them in order; the page's script keeps the list.
function chooseLanguages() {
  return (
    `<h2>Welcome to Measure Twice</h2>` +
    `<p>Which languages will you work in? Click them in order, <b>strongest ` +
    `first</b>: start with the one you know best and end with the one you're ` +
    `newest to. You can choose just one.</p>` +
    `<div class="row picker">` +
    LANGUAGES.map(([id, name]) => `<button data-pick="${id}">${name}</button>`).join("") +
    `</div>` +
    `<ol id="picked"></ol>` +
    `<p class="muted" id="picked-empty">None chosen yet.</p>` +
    `<div class="row"><button data-action="choose" id="choose" disabled>Start the guide</button>` +
    `<button data-pick-reset class="secondary">Clear</button></div>`
  );
}

function problems(state) {
  return (
    `<h2>Something needs fixing first</h2>` +
    `<p>The guide checked your toolchains before starting:</p>` +
    `<ul class="failures">` +
    (state.problems || []).map((p) => `<li><span class="bad">✗</span> ${escape(p)}</li>`).join("") +
    `</ul>` +
    `<p>Fix these, then start the guide again.</p>` +
    button("Start the guide", "start")
  );
}

// From a click on Start until the guide's first step is on screen. The shell
// starting and the toolchain check take a few seconds, and without this the
// panel looks as if nothing happened.
function startingUp() {
  return (
    `<h2>Starting the guide…</h2>` +
    `<p>It runs in the "Measure Twice guide" terminal. The first step shows ` +
    `here in a moment.</p>` +
    button("Show the guide's terminal", "terminal")
  );
}

function render(state, { trusted = true, needsLanguages = false, starting = false } = {}) {
  if (!trusted) {
    return untrusted();
  }
  if (starting || (state && state.status === "starting")) {
    return startingUp();
  }
  if (state && state.status === "problems") {
    return problems(state);
  }
  const running = state && ["setup", "testing", "ready"].includes(state.status);
  if (needsLanguages && !running) {
    return chooseLanguages();
  }
  if (state && state.status === "setup") {
    return (
      `<h2>Welcome to Measure Twice</h2>` +
      `<p>The guide is asking which languages you'll work in. Answer in its ` +
      `terminal: list your strongest first, for example <code>php python ts rust</code>, ` +
      `then press Enter.</p>` +
      button("Go to the guide's terminal", "terminal")
    );
  }
  if (!state || state.version !== 1 || !state.step) {
    return notRunning(state);
  }
  const { lesson, step, files, hints, progress } = state;
  const percent = progress.total ? Math.round((100 * progress.done) / progress.total) : 0;
  const out = [];

  out.push(
    `<p class="muted">Lesson ${lesson.number} of ${lesson.of} · ${escape(lesson.title)}` +
      ` · ${escape(state.language)}</p>`,
    `<div class="bar" title="${progress.done} of ${progress.total} guided steps done">` +
      `<div style="width:${percent}%"></div></div>`,
    `<h2>Step ${step.number} of ${step.of}: ${escape(step.title)}</h2>`,
  );
  // The guide stays on a finished step until the learner moves on, so they can
  // read what passed first.
  if (step.done) {
    out.push(
      `<div class="done"><p class="good"><b>✓ This step is done.</b></p>` +
        `<div class="row">${button("Next step →", "key", "n")}</div></div>`,
    );
  }
  if (step.intro) {
    out.push(`<div class="intro">${paragraphs(step.intro)}</div>`);
  }
  out.push(paragraphs(step.task));
  out.push(`<p class="next">${escape(step.next)}</p>`);

  const open = [button("Lesson README", "open", files.readme)];
  if (files.tests) open.push(button("Tests", "open", files.tests));
  if (files.edit) open.push(button("File you edit", "open", files.edit));
  out.push(`<div class="row">${open.join("")}</div>`);

  if (step.checklist.length) {
    out.push(
      "<h3>Checklist</h3><ul class=\"checklist\">" +
        step.checklist
          .map((item, i) => `<li><label><input type="checkbox" data-check="${i}"> ${escape(item)}</label></li>`)
          .join("") +
        "</ul>",
    );
  }
  if ((step.kind === "read" || step.kind === "confirm") && !step.done) {
    out.push(`<div class="row">${button("Done with this step", "key", "d")}</div>`);
  }

  out.push("<h3>Tests</h3>", results(state));

  out.push("<h3>Hints</h3>");
  out.push(
    hints.shown.map((h, i) => `<p class="hint"><b>Hint ${i + 1}:</b> ${escape(h)}</p>`).join(""),
  );
  const left = hints.total - hints.shown.length;
  if (hints.total === 0) {
    out.push(`<p class="muted">This step has no hints.</p>`);
  } else if (left > 0) {
    out.push(button(`Show a hint (${left} left)`, "key", "h"));
  } else {
    out.push(`<p class="muted">No more hints. The lesson README and the solutions branch are next.</p>`);
  }

  if (step.how_this_works) {
    out.push(`<div class="how">${paragraphs(step.how_this_works.replace(/\n/g, "\n\n"), "muted")}</div>`);
  }
  out.push(
    `<div class="row footer">${step.first ? "" : button("← Previous step", "key", "b")}` +
      `${button("Full test output", "key", "o")}` +
      `${button("Show the guide's terminal", "terminal")}</div>`,
  );
  return out.join("\n");
}

module.exports = { render, escape, paragraphs, LANGUAGES };
