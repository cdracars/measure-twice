import { defineConfig } from "vitest/config";

// Run from this folder: `npx vitest run` (scripts/check does this for you).
export default defineConfig({
  test: {
    include: ["*.test.ts"],
  },
});
