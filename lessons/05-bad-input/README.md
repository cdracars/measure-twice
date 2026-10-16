# Lesson 05: Bad input

**Stage 1 · Basics + TDD rhythm** · Languages: PHP · Python · TypeScript · Rust

## The problem

Until now, every function trusted its caller. Real input comes from people
typing, files, and other programs, and it's often wrong: `"abc"`, `"-5 g"`,
an empty line. Jig has to turn that text into its own types, and when it
can't, say *why* instead of crashing or, worse, quietly carrying on with a
nonsense value.

Lesson 03 also left a promise open: `consume` relied on every caller checking
`can_print` first. In this lesson the spool stops trusting its callers.

## What you write

| Function | Takes | Success | Failure |
| --- | --- | --- | --- |
| `parse_grams` | text like `"250"`, `"12.5 g"`, `" 40g "` | the number of grams | empty, not a number, or negative |
| `parse_material` | text like `"PLA"`, `" petg "` | a `Material` | unknown material |
| `Spool.consume` | grams | the spool has less filament | not enough filament, and the spool is unchanged |

Rules for `parse_grams`:

- Ignore spaces around the text, and an optional `g` at the end (with or
  without a space before it).
- Empty input (after trimming) is **empty**.
- Zero is fine. A negative number is **negative**.
- Anything else that isn't an ordinary decimal number is **not a number**,
  including `"nan"`, `"inf"`, `"0x10"`, and `"1_000"`.

Rules for `parse_material`: ignore surrounding spaces and letter case. Anything
else, including empty input, is an unknown material.

## Two ways to fail

This is the lesson's real subject. There are two main styles:

- **Exceptions** (PHP and Python here): the function *throws*, and the error
  travels up the call stack until something catches it. The function's
  signature doesn't mention it.
- **Errors as values** (Rust here, and TypeScript in this lesson): the
  function *returns* either a success or an error, and its signature says so.
  The caller has to look at the result to get the value out.

| | How failure is reported | What the caller writes |
| --- | --- | --- |
| PHP | `throw new NotANumber(...)` | `try { ... } catch (InvalidAmount $e) { ... }` |
| Python | `raise NotANumber(...)` | `try: ... except InvalidAmount: ...` |
| TypeScript | `return { ok: false, error: "not a number" }` | `if (!result.ok) { ... }` |
| Rust | `return Err(GramsError::NotANumber)` | `match result { Ok(g) => ..., Err(e) => ... }` or `?` |

The error types are already declared in each stub file; you write the
functions that use them.

TypeScript code more often throws exceptions. This lesson uses a result type
so you can compare the two styles side by side; you'll see both in real code.

## Your parser accepts things you didn't mean

Every language's built-in number parser is more generous than "an ordinary
decimal number". Here's what each one does with some awkward input, as
measured on this course's toolchain (Node 22, Python 3.13, PHP 8.3, Rust 1.97):

| Input | JS `Number()` | Python `float()` | PHP `is_numeric()` | Rust `parse::<f64>()` |
| --- | --- | --- | --- | --- |
| `""` | `0` | error | `false` | error |
| `"0x10"` | `16` | error | `false` | error |
| `"nan"` | `NaN` | `nan` | `false` | `Ok(NaN)` |
| `"inf"` | `NaN` | `inf` | `false` | `Ok(inf)` |
| `"Infinity"` | `Infinity` | `inf` | `false` | `Ok(inf)` |
| `"1_000"` | `NaN` | `1000.0` | `false` | error |

The tests include these cases. In each language, you'll need to reject some of
them yourself. A regular expression that describes the numbers you *do* accept
is one good approach; checking that the result is finite is another.

## New this lesson: you write the tests for `parse_material`

`parse_grams` and `consume` come with tests. `parse_material` comes with one
example. Write the rest before the code: different cases, surrounding spaces,
an unknown material, empty input.

## How to work through it

Start with the language you know best, then the ones you're learning, with
your weakest last.

1. **Red:** `./scripts/check 05 rust` (or `php`, `python`, `ts`)
2. **Green:** `parse_grams` first, then `consume`.
3. **Your tests:** write the `parse_material` tests, see them fail, then
   implement it.
4. **Refactor:** is the "strip spaces and a trailing g" step easy to read?

| Language | Stub you edit | Tests |
| --- | --- | --- |
| PHP | `php/parse.php` | `php/test.php` |
| Python | `python/parse.py` | `python/test_parse.py` |
| TypeScript | `ts/parse.ts` | `ts/parse.test.ts` |
| Rust | `rust/src/lib.rs` | `rust/tests/parse.rs` |

## What's different between the languages

| Question | PHP | Python | TypeScript | Rust |
| --- | --- | --- | --- | --- |
| Does the function signature say it can fail? | | | | |
| What happens if the caller ignores the failure? | | | | |
| How do you pass an error up to *your* caller? | | | | |
| How do you trim spaces from a string? | | | | |

Then answer in your own words:

- Rust's `?` operator and an uncaught exception both pass an error upward.
  What's the difference for someone *reading* the code?
- Why must `consume` leave the spool unchanged when it fails? What would go
  wrong later if it subtracted first and checked afterwards?

## Done when

- [ ] `./scripts/check 05` passes in all four languages
- [ ] You wrote the `parse_material` tests before its code, in each language
- [ ] You can explain, for one language, why `"nan"` needed special handling

**Read alongside:** *The Rust Programming Language*, chapter 9 ("Error
Handling"): <https://doc.rust-lang.org/book/>
