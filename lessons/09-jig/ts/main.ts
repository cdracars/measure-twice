// The entry point: the only code that touches the real terminal. Given.

import { run } from "./cli.ts";

// process.argv is [node, script, ...arguments].
const output = run(process.argv.slice(2));
process.stdout.write(output.stdout);
process.stderr.write(output.stderr);
process.exitCode = output.code;
