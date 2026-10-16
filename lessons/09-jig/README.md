# Lesson 09: Jig

**Stage 1 · Basics + TDD rhythm** · Languages: PHP · Python · TypeScript · Rust

## The problem

Eight lessons of pieces: filament math, materials, parsing, the Build Log.
Now you put them behind a real command-line tool:

```console
$ jig grams 1000 PLA
2.98 g
$ jig check petg 200
too cold: PETG prints at 220–250 °C
$ jig log workshop.log
entries: 3
problems: 3
  line 4: missing separator
  line 6: bad date
  line 7: empty text
```

The pieces from earlier lessons are given, finished, in `workshop.*` (and
`workshop.rs`). You write the part that turns command-line arguments into
output: the **command-line interface**.

## The big idea: keep the logic pure, the I/O at the edge

A command-line program reads arguments, prints to the screen, and exits with
a status code. All three are awkward to test directly. So the work is split:

- **`run(args)`** is a plain function. It takes the arguments as a list of
  strings and *returns* an `Output`: an exit code, the text for standard
  output, and the text for standard error. It never prints and never exits.
  This is what you write, and what the tests call.
- **The entry point** (`jig.php`, `jig.py`, `main.ts`, `main.rs`) is a few
  given lines: read the real arguments, call `run`, print, exit.

Because `run` is pure, the tests need no terminal, no subprocess, and no
mocking. This split goes by several names, such as "functional core,
imperative shell" or "humble object", and it's the first architecture lesson
in disguise. You started this in lesson 08's refactor step.

## What `run` must do

Commands:

| Arguments | Standard output | Exit code |
| --- | --- | --- |
| `help` | the usage text | 0 |
| *(none)* | nothing; usage text on standard **error** | 2 |
| `grams <length-mm> <material>` | the weight of that much 1.75 mm filament, two decimals: `2.98 g` | 0 |
| `check <material> <nozzle-c>` | `ok: PLA prints at 190–220 °C`, or `too cold: …` / `too hot: …` | 0 if ok, 1 if not |
| `log <file>` | a summary of the Build Log (see below) | 0 if no problems, 1 if any |

Errors go to standard error, start with `jig: `, and exit with code 2:

| Situation | Standard error |
| --- | --- |
| Unknown command `frobnicate` | `jig: unknown command: frobnicate` then `run 'jig help' to see the commands` |
| Wrong number of arguments to `grams` | `jig: usage: jig grams <length-mm> <material>` |
| Wrong number of arguments to `check` | `jig: usage: jig check <material> <nozzle-c>` |
| Wrong number of arguments to `log` | `jig: usage: jig log <file>` |
| Unknown material | `jig: unknown material: Nylon` |
| Bad length | `jig: not a length: abc` |
| Bad temperature | `jig: not a temperature: hot` |
| Missing log file | `jig: no such file: <path>` |

Material names are accepted in any case, and printed in capitals (`PETG`).
Every line of output, including the last, ends with a newline.

The usage text is given in each stub as `USAGE`.

### The `log` summary

```text
entries: 3
problems: 3
  line 4: missing separator
  line 6: bad date
  line 7: empty text
```

One line per problem, indented two spaces, in file order. A log with no
problems prints just the two count lines.

### Exit codes

0 means success. For a question like "is this temperature OK?", many tools use
1 for "ran fine, and the answer is no" and 2 for "you used me wrong". `grep`
works this way: 0 if it found a match, 1 if it didn't, 2 on an error. Scripts
rely on that difference.

## New this lesson: you write every test for one command

`help`, `grams`, `check`, and the error cases come with tests. The `log`
command comes with **none**. Write its tests from the spec above, before the
code. Lesson 08's `fixtures/workshop.log` and `fixtures/empty.log` are good
inputs; you'll also want one for a missing file.

## How to work through it

Start with the language you know best, then the ones you're learning, with
your weakest last.

1. **Red:** `./scripts/check 09 rust` (or `php`, `python`, `ts`)
2. **Green:** `help`, then `grams`, then `check`.
3. **Your tests:** write the `log` tests, see them fail, then implement it.
4. **Refactor:** `run` will grow into a long branch. Would one function per
   command read better?
5. **Try it for real:**

| Language | Run it |
| --- | --- |
| PHP | `php lessons/09-jig/php/jig.php grams 1000 PLA` |
| Python | `python3 lessons/09-jig/python/jig.py grams 1000 PLA` |
| TypeScript | `node lessons/09-jig/ts/main.ts grams 1000 PLA` |
| Rust | `cargo run -q -p lesson-09-jig -- grams 1000 PLA` |

Check the exit code afterwards with `echo $?`.

| Language | Stub you edit | Given | Tests |
| --- | --- | --- | --- |
| PHP | `php/cli.php` | `php/workshop.php`, `php/jig.php` | `php/test.php` |
| Python | `python/cli.py` | `python/workshop.py`, `python/jig.py` | `python/test_cli.py` |
| TypeScript | `ts/cli.ts` | `ts/workshop.ts`, `ts/main.ts` | `ts/cli.test.ts` |
| Rust | `rust/src/lib.rs` | `rust/src/workshop.rs`, `rust/src/main.rs` | `rust/tests/cli.rs` |

## What's different between the languages

| Question | PHP | Python | TypeScript | Rust |
| --- | --- | --- | --- | --- |
| Where do the command-line arguments come from? | | | | |
| Is the program's own name in that list? | | | | |
| How do you print to standard error? | | | | |
| How do you set the exit code? | | | | |

Then answer in your own words:

- Why should errors go to standard error instead of standard output? (Try
  `jig grams abc PLA > out.txt` with each choice.)
- Your tests never started a process. What *isn't* tested, then? How small
  is that untested part, and why is that acceptable?

## Done when

- [ ] `./scripts/check 09` passes in all four languages
- [ ] You wrote every `log` test before implementing `log`
- [ ] You ran `jig` from the terminal in at least two languages and checked
      the exit codes

That's the end of stage 1. Stage 2 starts by moving these tests onto real
test frameworks.

**Read alongside:** *The Rust Programming Language*, chapter 12 ("An I/O
Project: Building a Command Line Program"): <https://doc.rust-lang.org/book/>
