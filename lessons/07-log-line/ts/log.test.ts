import assert from "node:assert/strict";
import { describe, test } from "node:test";

import { formatEntry, parseEntry, truncate } from "./log.ts";

describe("truncate", () => {
  test("short text is unchanged", () => {
    assert.equal(truncate("benchy", 10), "benchy");
  });

  test("text exactly at the limit is unchanged", () => {
    assert.equal(truncate("1234567890", 10), "1234567890");
  });

  test("long text is cut and marked", () => {
    assert.equal(truncate("replaced the nozzle", 8), "replaced…");
  });

  test("a degree sign counts as one character", () => {
    assert.equal(truncate("nozzle at 215 °C", 15), "nozzle at 215 °…");
  });

  test("an emoji counts as one character", () => {
    assert.equal(truncate("new spool 🧵 loaded", 11), "new spool 🧵…");
  });
});

describe("formatEntry", () => {
  test("format an entry", () => {
    assert.equal(formatEntry({ date: "2026-10-16", text: "replaced nozzle" }), "2026-10-16: replaced nozzle");
  });
});

// Two examples. Write the error tests before the code.
describe("parseEntry", () => {
  test("parse a simple line", () => {
    assert.deepEqual(parseEntry("2026-10-16: replaced nozzle"), {
      ok: true,
      value: { date: "2026-10-16", text: "replaced nozzle" },
    });
  });

  test("parse ignores surrounding spaces", () => {
    assert.deepEqual(parseEntry("  2026-10-17 :   raised Z offset  "), {
      ok: true,
      value: { date: "2026-10-17", text: "raised Z offset" },
    });
  });
});
