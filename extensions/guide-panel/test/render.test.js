// Run: node --test "extensions/guide-panel/test/*.test.js"

"use strict";

const assert = require("node:assert/strict");
const { test } = require("node:test");
const { render, paragraphs } = require("../render");

function state(overrides = {}) {
  return {
    version: 1,
    status: "ready",
    pids: [1234],
    lesson: { number: 1, of: 10, title: "Filament math" },
    language: "PHP",
    progress: { done: 0, total: 20 },
    step: {
      number: 1,
      of: 5,
      title: "Read your teammate's tests",
      kind: "read",
      intro: "This lesson teaches TDD.\n\nThe setup: a teammate wrote tests.",
      task: "Before any code, read the tests\nyou've been handed.",
      next: "Next: open lessons/01-filament-math/php/test.php. No code yet.",
      how_this_works: "How this works: red.\nStuck? Type h.",
      checklist: ["Read \"The problem\"", "Find the first test"],
    },
    files: {
      readme: "lessons/01-filament-math/README.md",
      tests: "lessons/01-filament-math/php/test.php",
      edit: "lessons/01-filament-math/php/filament.php",
    },
    files_open: true,
    hints: { shown: [], total: 0 },
    results: {
      ran: true,
      passing: 0,
      failing: [{ name: "one metre weighs about 3 g", message: "TODO: implement filament_grams" }],
      notice: "These fail because there's no code yet.",
      tone: "quiet",
    },
    ...overrides,
  };
}

test("in Restricted Mode it asks for trust instead of showing the step", () => {
  const html = render(state(), { trusted: false });
  assert.match(html, /Trust this folder to start/);
  assert.match(html, /data-action="trust"/);
  assert.doesNotMatch(html, /Step 1 of 5/);
});

test("a stopped guide offers to start it", () => {
  const html = render({ version: 1, status: "stopped" });
  assert.match(html, /isn't running/);
  assert.match(html, /data-action="start"/);
});

test("no state file at all also offers to start the guide", () => {
  assert.match(render(null), /data-action="start"/);
});

test("finishing every step says so", () => {
  assert.match(render({ version: 1, status: "all-done" }), /finished every guided step/);
});

test("the step shows its lesson, title, intro, task and next line", () => {
  const html = render(state());
  assert.match(html, /Lesson 1 of 10 · Filament math · PHP/);
  assert.match(html, /Step 1 of 5: Read your teammate's tests/);
  assert.match(html, /This lesson teaches TDD\./);
  assert.match(html, /Before any code, read the tests you've been handed\./);
  assert.match(html, /Next: open lessons\/01-filament-math\/php\/test\.php/);
});

test("each file gets an open button", () => {
  const html = render(state());
  for (const file of ["README.md", "php/test.php", "php/filament.php"]) {
    assert.ok(html.includes(`data-action="open" data-value="lessons/01-filament-math/${file}"`), file);
  }
});

test("a read step has its checklist and a done button that types d", () => {
  const html = render(state());
  assert.match(html, /data-check="1"/);
  assert.match(html, /data-action="key" data-value="d"/);
});

test("a check step has no done button", () => {
  const html = render(state({ step: { ...state().step, kind: "check", checklist: [] } }));
  assert.doesNotMatch(html, /data-value="d"/);
});

test("failures show their name and message", () => {
  const html = render(state());
  assert.match(html, /one metre weighs about 3 g/);
  assert.match(html, /TODO: implement filament_grams/);
  assert.match(html, /class="quiet">These fail because there's no code yet\./);
});

test("while the tests run, it says so instead of showing old results", () => {
  const html = render(state({ status: "testing", results: null }));
  assert.match(html, /Running the tests/);
});

test("the hint button counts down and stops when hints run out", () => {
  const some = render(state({ hints: { shown: ["Look at the formula."], total: 3 } }));
  assert.match(some, /Hint 1:<\/b> Look at the formula\./);
  assert.match(some, /Show a hint \(2 left\)/);
  const none = render(state({ hints: { shown: ["a", "b", "c"], total: 3 } }));
  assert.match(none, /No more hints/);
});

test("text from the guide is escaped", () => {
  const html = render(state({ step: { ...state().step, title: "<script>alert(1)</script>" } }));
  assert.doesNotMatch(html, /<script>/);
  assert.match(html, /&lt;script&gt;/);
});

test("wrapped lines join into paragraphs; blank lines split them", () => {
  assert.equal(paragraphs("one\ntwo\n\nthree"), "<p>one two</p><p>three</p>");
});
