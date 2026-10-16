import assert from "node:assert/strict";
import { copyFileSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterEach, beforeEach, describe, test } from "node:test";

import { type LoadedLog, type LogEntry, appendEntry, formatEntry, loadLog } from "./build_log.ts";

const fixtures = join(import.meta.dirname, "..", "fixtures");

/** The loaded log, failing the test if the file couldn't be read. */
function load(path: string): LoadedLog {
  const result = loadLog(path);
  assert.ok(result.ok, `could not load ${path}`);
  return result.value;
}

function lines(entries: LogEntry[]): string[] {
  return entries.map(formatEntry);
}

describe("loadLog", () => {
  test("loads the good entries in order", () => {
    assert.deepEqual(lines(load(join(fixtures, "workshop.log")).entries), [
      "2026-10-14: new 0.4 mm nozzle",
      "2026-10-16: replaced PTFE tube",
      "2026-10-18: note: PETG strings above 245 °C",
    ]);
  });

  test("reports each bad line with its line number and error", () => {
    assert.deepEqual(load(join(fixtures, "workshop.log")).problems, [
      { lineNumber: 4, error: "missing separator" },
      { lineNumber: 6, error: "bad date" },
      { lineNumber: 7, error: "empty text" },
    ]);
  });

  test("an empty file has no entries and no problems", () => {
    assert.deepEqual(load(join(fixtures, "empty.log")), { entries: [], problems: [] });
  });

  test("Windows line endings are handled", () => {
    const entries = load(join(fixtures, "windows.log")).entries;
    assert.deepEqual(
      entries.map((e) => e.text),
      ["new nozzle", "dried PETG"],
    );
  });

  test("a missing file is reported", () => {
    assert.deepEqual(loadLog(join(fixtures, "no-such-file.log")), { ok: false, error: "not found" });
  });
});

// One example. Write the rest before the code.
describe("appendEntry", () => {
  // A new, empty directory for each test, deleted afterwards.
  let dir = "";
  beforeEach(() => {
    dir = mkdtempSync(join(tmpdir(), "measure-twice-"));
  });
  afterEach(() => {
    rmSync(dir, { recursive: true, force: true });
  });

  test("appending to a new file creates it", () => {
    const path = join(dir, "build.log");
    appendEntry(path, { date: "2026-10-19", text: "levelled the bed" });
    assert.deepEqual(lines(load(path).entries), ["2026-10-19: levelled the bed"]);
  });

  test("appending twice keeps the order", () => {
    const path = join(dir, "build.log");
    appendEntry(path, { date: "2026-10-19", text: "levelled the bed" });
    appendEntry(path, { date: "2026-10-20", text: "printed a calibration cube" });
    assert.deepEqual(lines(load(path).entries), [
      "2026-10-19: levelled the bed",
      "2026-10-20: printed a calibration cube",
    ]);
  });

  test("appending to an existing log keeps what was there", () => {
    const path = join(dir, "build.log");
    copyFileSync(join(fixtures, "workshop.log"), path);
    appendEntry(path, { date: "2026-10-19", text: "levelled the bed" });
    const log = load(path);
    assert.equal(log.entries.length, 4);
    assert.equal(formatEntry(log.entries[3]!), "2026-10-19: levelled the bed");
    assert.equal(log.problems.length, 3);
  });
});
