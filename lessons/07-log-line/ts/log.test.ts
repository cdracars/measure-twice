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

  test("a colon inside the text is kept", () => {
    const result = parseEntry("2026-10-18: note: PETG strings");
    assert.ok(result.ok);
    assert.equal(result.value.text, "note: PETG strings");
  });

  test("format undoes parse", () => {
    const line = "2026-10-18: note: PETG strings above 245 °C";
    const result = parseEntry(line);
    assert.ok(result.ok);
    assert.equal(formatEntry(result.value), line);
  });

  test("a line without a colon is missing its separator", () => {
    assert.deepEqual(parseEntry("2026-10-16 replaced nozzle"), { ok: false, error: "missing separator" });
  });

  for (const date of ["16/10/2026", "2026-13-01", "2026-00-10", "2026-10-32", "2026-10-00", "2026-1-5", ""]) {
    test(`${JSON.stringify(date)} is a bad date`, () => {
      assert.deepEqual(parseEntry(`${date}: replaced nozzle`), { ok: false, error: "bad date" });
    });
  }

  test("blank text is empty", () => {
    assert.deepEqual(parseEntry("2026-10-16:   "), { ok: false, error: "empty text" });
  });
});
