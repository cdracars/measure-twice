import assert from "node:assert/strict";
import { describe, test } from "node:test";

import { type GramsError, Spool, parseGrams, parseMaterial } from "./parse.ts";

describe("parseGrams", () => {
  const accepted: [string, number][] = [
    ["250", 250],
    ["12.5", 12.5],
    ["12.5 g", 12.5],
    ["40g", 40],
    [" 40g ", 40],
    ["0", 0],
  ];
  for (const [text, grams] of accepted) {
    test(`accepts ${JSON.stringify(text)}`, () => {
      assert.deepEqual(parseGrams(text), { ok: true, value: grams });
    });
  }

  const rejected: [string, GramsError][] = [
    ["", "empty"],
    ["   ", "empty"],
    ["abc", "not a number"],
    ["12.5 kg", "not a number"],
    ["nan", "not a number"],
    ["inf", "not a number"],
    ["0x10", "not a number"],
    ["1_000", "not a number"],
    ["-5", "negative"],
    ["-5 g", "negative"],
  ];
  for (const [text, error] of rejected) {
    test(`rejects ${JSON.stringify(text)} as ${error}`, () => {
      assert.deepEqual(parseGrams(text), { ok: false, error });
    });
  }
});

describe("Spool.consume", () => {
  test("consuming what is available works", () => {
    const spool = new Spool(100);
    assert.deepEqual(spool.consume(40), { ok: true, value: undefined });
    assert.equal(spool.gramsRemaining, 60);
  });

  test("consuming exactly what is left works", () => {
    const spool = new Spool(100);
    assert.equal(spool.consume(100).ok, true);
    assert.equal(spool.gramsRemaining, 0);
  });

  test("consuming more than is left is refused", () => {
    const spool = new Spool(100);
    assert.deepEqual(spool.consume(100.5), {
      ok: false,
      error: { needed: 100.5, remaining: 100 },
    });
  });

  test("a refused consume leaves the spool unchanged", () => {
    const spool = new Spool(100);
    spool.consume(150);
    assert.equal(spool.gramsRemaining, 100);
  });
});

// One example. Write the rest before the code.
describe("parseMaterial", () => {
  test("accepts PLA", () => {
    assert.deepEqual(parseMaterial("PLA"), { ok: true, value: "PLA" });
  });

  test("ignores case", () => {
    assert.deepEqual(parseMaterial("petg"), { ok: true, value: "PETG" });
    assert.deepEqual(parseMaterial("Tpu"), { ok: true, value: "TPU" });
  });

  test("ignores surrounding spaces", () => {
    assert.deepEqual(parseMaterial("  ABS "), { ok: true, value: "ABS" });
  });

  test("rejects an unknown material", () => {
    assert.deepEqual(parseMaterial("Nylon"), { ok: false, error: "unknown material" });
  });

  test("rejects empty input", () => {
    assert.deepEqual(parseMaterial(""), { ok: false, error: "unknown material" });
  });
});
