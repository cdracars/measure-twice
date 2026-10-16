# Lesson 07: Log line

**Stage 1 · Basics + TDD rhythm** · Languages: PHP · Python · TypeScript · Rust

## The problem

Jig's **Build Log** is plain text, one entry per line:

```text
2026-10-16: replaced nozzle
2026-10-17: first layer too squished, raised Z offset 0.05 mm
2026-10-18: note: PETG strings above 245 °C
```

In this lesson you turn one line into a `LogEntry` (a date and some text),
turn an entry back into a line, and shorten long text for display without
breaking it. Text is where languages differ most, and where Unicode quietly
breaks code that works fine on plain English.

## What you write

| Function | Takes | Returns |
| --- | --- | --- |
| `parse_entry` | one line | a `LogEntry`, or an error |
| `format_entry` | a `LogEntry` | the line again, as `YYYY-MM-DD: text` |
| `truncate` | text and a maximum number of characters | the text unchanged if it fits; otherwise the first *max* characters followed by `…` |

(TypeScript: `parseEntry`, `formatEntry`, `truncate`.)

Rules for `parse_entry`:

- The date and text are split at the **first** colon. The text may contain
  more colons (`note: PETG strings…`).
- Spaces around the date and around the text are ignored.
- No colon at all is a **missing separator** error.
- The date must look like `YYYY-MM-DD`, with a month from 01 to 12 and a day
  from 01 to 31. Anything else is a **bad date**. (This checks the shape
  only: `2026-02-30` passes. A real date library would catch it; stage 2
  uses one.)
- Blank text is an **empty text** error.

The `LogEntry` type and the error types are given in each stub file, using
the same style as lesson 05: exceptions in PHP and Python, result values in
TypeScript and Rust.

## "Character" is harder than it looks

`truncate` counts *characters*, but each language's default string length
and slicing count something else. Measured on this course's toolchain:

| | Default length counts | Slicing `"nozzle at 215 °C"` after 15 | Character-safe way |
| --- | --- | --- | --- |
| PHP | bytes: `strlen` is 17 | `substr` cuts `°` in half and leaves a broken byte | `mb_strlen`, `mb_substr` (the `mbstring` extension) |
| Python | characters: `len` is 16 | correct | the default |
| TypeScript | UTF-16 units: `"🧵".length` is 2 | `slice` on `"new spool 🧵 loaded"` splits the emoji in two | `[...text]` or `Array.from(text)` |
| Rust | bytes: `len` is 17 | `&text[..15]` **panics**: "byte index 15 is not a char boundary" | `text.chars()` |

The tests include `°` and `🧵`, so the default slicing will fail in three of
the four languages. That's deliberate.

One step further, which this lesson doesn't test: some things a reader sees as
one character are several code points (flags, emoji with skin tones, letters
with combining accents). Handling those properly means "grapheme clusters",
and none of the four standard libraries does it by default.

## New this lesson: you write the error tests

`truncate` and `format_entry` come with tests. `parse_entry` comes with two
examples. Write tests for each error rule above before you write the code,
plus at least one test for a colon inside the text.

## How to work through it

Start with the language you know best, then the ones you're learning, with
your weakest last.

1. **Red:** `./scripts/check 07 rust` (or `php`, `python`, `ts`)
2. **Green:** `truncate` and `format_entry`.
3. **Your tests:** write the `parse_entry` error tests, see them fail, then
   implement it.
4. **Refactor:** is the date check readable? Would a named helper help?

| Language | Stub you edit | Tests |
| --- | --- | --- |
| PHP | `php/log.php` | `php/test.php` |
| Python | `python/log.py` | `python/test_log.py` |
| TypeScript | `ts/log.ts` | `ts/log.test.ts` |
| Rust | `rust/src/lib.rs` | `rust/tests/log.rs` |

## What's different between the languages

| Question | PHP | Python | TypeScript | Rust |
| --- | --- | --- | --- | --- |
| How do you split a string at the first `:` only? | | | | |
| How do you build `date + ": " + text`? | | | | |
| Can you change a string in place? | | | | |
| What does `truncate` return: a new string, or part of the old one? | | | | |

Then answer in your own words:

- Rust has two string types, `String` (owned, growable) and `&str` (a
  borrowed view into some string's bytes). `parse_entry` takes a `&str` but
  `LogEntry` stores `String`s. Why? What would `LogEntry` need if it stored
  `&str` instead? (Look up "lifetimes" in the Rust book, chapter 10.3.)
- Why does Rust panic on `&text[..15]` instead of quietly returning broken
  text like PHP's `substr`? Which behaviour would you rather debug?

## Done when

- [ ] `./scripts/check 07` passes in all four languages
- [ ] You wrote a test for every `parse_entry` error rule, before the code
- [ ] You can explain what each language's default string length counts

**Read alongside:** *The Rust Programming Language*, chapter 8.2 ("Storing
UTF-8 Encoded Text with Strings"): <https://doc.rust-lang.org/book/>
