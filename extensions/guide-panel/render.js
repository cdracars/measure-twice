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
  if (r.ran && r.passing) {
    parts.push(`<p class="good">✓ ${r.passing} passing</p>`);
  }
  if (r.failing.length) {
    parts.push(
      "<ul class=\"failures\">" +
        r.failing
          .map(
            (f) =>
              `<li><span class="bad">✗</span> ${escape(f.name)}` +
              (f.message ? `<div class="message">${escape(f.message)}</div>` : "") +
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

function render(state, { trusted = true } = {}) {
  if (!trusted) {
    return untrusted();
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
  if (step.kind === "read" || step.kind === "confirm") {
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
    `<div class="row footer">${button("Full test output", "key", "o")}` +
      `${button("Show the guide's terminal", "terminal")}</div>`,
  );
  return out.join("\n");
}

module.exports = { render, escape, paragraphs };
