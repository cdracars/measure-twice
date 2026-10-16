import assert from "node:assert/strict";
import { describe, test } from "node:test";

import { needsEnclosure, nozzleVerdict } from "./temperature.ts";

describe("nozzleVerdict", () => {
  test("PLA in the middle of its range is ok", () => {
    assert.equal(nozzleVerdict("PLA", 205), "ok");
  });

  test("PLA at its minimum is ok", () => {
    assert.equal(nozzleVerdict("PLA", 190), "ok");
  });

  test("PLA one degree below its minimum is too cold", () => {
    assert.equal(nozzleVerdict("PLA", 189), "too cold");
  });

  test("PLA at its maximum is ok", () => {
    assert.equal(nozzleVerdict("PLA", 220), "ok");
  });

  test("PLA one degree above its maximum is too hot", () => {
    assert.equal(nozzleVerdict("PLA", 221), "too hot");
  });

  test("PETG at a PLA temperature is too cold", () => {
    assert.equal(nozzleVerdict("PETG", 200), "too cold");
  });

  test("ABS at its maximum is ok", () => {
    assert.equal(nozzleVerdict("ABS", 260), "ok");
  });

  test("TPU above its maximum is too hot", () => {
    assert.equal(nozzleVerdict("TPU", 231), "too hot");
  });

  test("an unknown material is reported", () => {
    assert.equal(nozzleVerdict("Nylon", 250), "unknown material");
  });

  test("material names are exact", () => {
    assert.equal(nozzleVerdict("pla", 205), "unknown material");
  });
});

// One example. Write the rest before the code.
describe("needsEnclosure", () => {
  test("ABS needs an enclosure", () => {
    assert.equal(needsEnclosure("ABS"), true);
  });

  for (const material of ["PLA", "PETG", "TPU", "Nylon"]) {
    test(`${material} does not need an enclosure`, () => {
      assert.equal(needsEnclosure(material), false);
    });
  }
});
