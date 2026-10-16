import assert from "node:assert/strict";
import { join } from "node:path";
import { describe, test } from "node:test";

import { type Output, USAGE, run } from "./cli.ts";

function output(code: number, streams: { stdout?: string; stderr?: string }): Output {
  return { code, stdout: streams.stdout ?? "", stderr: streams.stderr ?? "" };
}

describe("help and errors", () => {
  test("help prints the usage", () => {
    assert.deepEqual(run(["help"]), output(0, { stdout: USAGE }));
  });

  test("no arguments prints the usage as an error", () => {
    assert.deepEqual(run([]), output(2, { stderr: USAGE }));
  });

  test("an unknown command is an error", () => {
    assert.deepEqual(
      run(["frobnicate"]),
      output(2, { stderr: "jig: unknown command: frobnicate\nrun 'jig help' to see the commands\n" }),
    );
  });
});

describe("grams", () => {
  test("grams of PLA", () => {
    assert.deepEqual(run(["grams", "1000", "PLA"]), output(0, { stdout: "2.98 g\n" }));
  });

  test("accepts a lowercase material", () => {
    assert.deepEqual(run(["grams", "4200", "petg"]), output(0, { stdout: "12.83 g\n" }));
  });

  test("rejects a bad length", () => {
    assert.deepEqual(run(["grams", "abc", "PLA"]), output(2, { stderr: "jig: not a length: abc\n" }));
  });

  test("rejects an unknown material", () => {
    assert.deepEqual(run(["grams", "1000", "Nylon"]), output(2, { stderr: "jig: unknown material: Nylon\n" }));
  });

  test("needs exactly two arguments", () => {
    assert.deepEqual(
      run(["grams", "1000"]),
      output(2, { stderr: "jig: usage: jig grams <length-mm> <material>\n" }),
    );
  });
});

describe("check", () => {
  test("a good temperature", () => {
    assert.deepEqual(run(["check", "PLA", "205"]), output(0, { stdout: "ok: PLA prints at 190–220 °C\n" }));
  });

  test("a cold temperature", () => {
    assert.deepEqual(
      run(["check", "petg", "200"]),
      output(1, { stdout: "too cold: PETG prints at 220–250 °C\n" }),
    );
  });

  test("a hot temperature", () => {
    assert.deepEqual(run(["check", "TPU", "240"]), output(1, { stdout: "too hot: TPU prints at 210–230 °C\n" }));
  });

  test("rejects a bad temperature", () => {
    assert.deepEqual(run(["check", "PLA", "hot"]), output(2, { stderr: "jig: not a temperature: hot\n" }));
  });

  test("needs exactly two arguments", () => {
    assert.deepEqual(
      run(["check", "PLA", "205", "extra"]),
      output(2, { stderr: "jig: usage: jig check <material> <nozzle-c>\n" }),
    );
  });
});

// No tests yet. Write them before the code.
describe("log", () => {
  const fixtures = join(import.meta.dirname, "..", "..", "08-build-log", "fixtures");

  test("summarizes a log with problems", () => {
    assert.deepEqual(
      run(["log", join(fixtures, "workshop.log")]),
      output(1, { stdout: "entries: 3\nproblems: 3\n  line 4: missing separator\n  line 6: bad date\n  line 7: empty text\n" }),
    );
  });

  test("a clean log succeeds", () => {
    assert.deepEqual(run(["log", join(fixtures, "windows.log")]), output(0, { stdout: "entries: 2\nproblems: 0\n" }));
  });

  test("an empty file", () => {
    assert.deepEqual(run(["log", join(fixtures, "empty.log")]), output(0, { stdout: "entries: 0\nproblems: 0\n" }));
  });

  test("a missing file is an error", () => {
    const path = join(fixtures, "no-such-file.log");
    assert.deepEqual(run(["log", path]), output(2, { stderr: `jig: no such file: ${path}\n` }));
  });

  test("needs exactly one argument", () => {
    assert.deepEqual(run(["log"]), output(2, { stderr: "jig: usage: jig log <file>\n" }));
  });
});
