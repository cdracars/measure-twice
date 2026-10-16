# Lesson 08: Build Log

**Stage 1 · Basics + TDD rhythm** · Languages: PHP · Python · TypeScript · Rust

## The problem

Lesson 07 parsed one line. A real **Build Log** is a file: dozens of lines,
some blank, some comments, a few typed in a hurry and wrong. Jig should load
every good entry, and report the bad lines by line number instead of giving
up on the whole file at the first mistake. It should also be able to add a
new entry to the end of the file.

```text
# Workshop build log
2026-10-14: new 0.4 mm nozzle

2026-10-15 calibrated e-steps        ← missing the colon
2026-10-16: replaced PTFE tube
2026-13-01: impossible date          ← month 13
2026-10-17:                          ← no text
2026-10-18: note: PETG strings above 245 °C
```

That's `fixtures/workshop.log`. The tests read it, along with two other
fixtures: an empty file, and `fixtures/windows.log`, which has Windows line
endings (`\r\n` instead of `\n`).

## What you write

| Function | Does |
| --- | --- |
| `load_log(path)` | Reads the file and returns its **entries** plus a list of **problems**: one per bad line, with its line number (counting from 1) and the lesson 07 error. Blank lines and lines starting with `#` are skipped. |
| `append_entry(path, entry)` | Adds the entry as a new line at the end of the file, creating the file if it doesn't exist. |

(TypeScript: `loadLog`, `appendEntry`.)

Lesson 07's `parse_entry` and `format_entry` are included, finished, in each
stub file. If you haven't done lesson 07 yet, do it first; this lesson
builds on it.

### When the file doesn't exist

Each language has its own normal way to report a missing file, and this lesson
uses it:

| | Missing file |
| --- | --- |
| PHP | throws `LogFileNotFound` (given). Careful: `file_get_contents` on a missing file doesn't throw; it returns `false` and prints a warning. |
| Python | raises the built-in `FileNotFoundError`. `open()` already does this. |
| TypeScript | returns `{ ok: false, error: "not found" }`. Node's `readFileSync` *throws* an error whose `code` is `"ENOENT"`; you catch it and convert it. |
| Rust | returns `Err` with a `std::io::Error` whose `kind()` is `NotFound`. `std::fs::read_to_string` already does this, and `?` passes it up. |

### Windows line endings

Splitting `windows.log` on `\n` leaves a `\r` at the end of every line. In
this lesson that's harmless *only* because `parse_entry` trims the text. In
other code it's a classic source of "the strings look equal but aren't" bugs.
The test that loads `windows.log` checks the entries come out clean.

## New this lesson: tests that touch the file system

`load_log` comes with tests. `append_entry` comes with one example. Write the
rest before the code: appending twice keeps the order; appending to an
existing log keeps what was there.

Tests that write files need somewhere safe to write. Never write into the
repository; use a fresh temporary directory per test, so tests can't affect
each other or leave junk behind. The example test shows how in each language.

## How to work through it

Start with the language you know best, then the ones you're learning, with
your weakest last.

1. **Red:** `./scripts/check 08 rust` (or `php`, `python`, `ts`)
2. **Green:** `load_log`.
3. **Your tests:** write the `append_entry` tests, see them fail, then
   implement it.
4. **Refactor:** `load_log` reads a file *and* interprets lines. Could the
   interpreting part be a separate function that takes text, so most tests
   wouldn't need files at all? (This idea is the heart of the architecture
   track: keep the logic pure and the file access at the edge.)

| Language | Stub you edit | Tests |
| --- | --- | --- |
| PHP | `php/build_log.php` | `php/test.php` |
| Python | `python/build_log.py` | `python/test_build_log.py` |
| TypeScript | `ts/build_log.ts` | `ts/build_log.test.ts` |
| Rust | `rust/src/lib.rs` | `rust/tests/build_log.rs` |

## What's different between the languages

| Question | PHP | Python | TypeScript | Rust |
| --- | --- | --- | --- | --- |
| How do you read a whole file into a string? | | | | |
| How do you append to a file? | | | | |
| How do you make a temporary directory? | | | | |
| How does a test find the fixtures folder? | | | | |
| Is the file closed for you when you're done? | | | | |

Then answer in your own words:

- Why report problems with line numbers instead of stopping at the first bad
  line? When *would* stopping at the first error be the better choice?

## Done when

- [ ] `./scripts/check 08` passes in all four languages
- [ ] You wrote the `append_entry` tests before its code, each using a fresh
      temporary directory
- [ ] You can explain where the `\r` comes from in `windows.log`, and why it
      didn't break anything here

**Read alongside:** *The Rust Programming Language*, chapter 12 ("An I/O
Project: Building a Command Line Program"), especially 12.2 and 12.3:
<https://doc.rust-lang.org/book/>
