import assert from "node:assert/strict";
import { describe, test } from "node:test";

import { type Job, gramsByMaterial, heaviestJob, jobsUsing, totalGrams } from "./batch.ts";

function fridayQueue(): Job[] {
  return [
    { name: "benchy", material: "PLA", grams: 12.5 },
    { name: "bracket", material: "PETG", grams: 40 },
    { name: "phone case", material: "TPU", grams: 22.25 },
    { name: "vase", material: "PLA", grams: 85 },
    { name: "enclosure hinge", material: "ABS", grams: 7.75 },
  ];
}

describe("batch", () => {
  test("total grams of a batch", () => {
    assert.equal(totalGrams(fridayQueue()), 167.5);
  });

  test("total grams of no jobs is zero", () => {
    assert.equal(totalGrams([]), 0);
  });

  test("grams by material", () => {
    assert.deepEqual(
      gramsByMaterial(fridayQueue()),
      new Map([
        ["PLA", 97.5],
        ["PETG", 40],
        ["TPU", 22.25],
        ["ABS", 7.75],
      ]),
    );
  });

  test("grams by material leaves out materials that are not used", () => {
    const jobs: Job[] = [{ name: "benchy", material: "PLA", grams: 12.5 }];
    assert.deepEqual(gramsByMaterial(jobs), new Map([["PLA", 12.5]]));
  });

  test("jobs using PLA, in order", () => {
    assert.deepEqual(jobsUsing(fridayQueue(), "PLA"), ["benchy", "vase"]);
  });

  test("jobs using a material nobody uses", () => {
    const jobs: Job[] = [{ name: "benchy", material: "PLA", grams: 12.5 }];
    assert.deepEqual(jobsUsing(jobs, "ABS"), []);
  });
});

// One example. Write the tricky cases before the code.
describe("heaviestJob", () => {
  test("the heaviest job in the batch", () => {
    assert.equal(heaviestJob(fridayQueue())?.name, "vase");
  });
});
