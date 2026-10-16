# Lesson 01: Filament math

**Stage 1 · Basics + TDD rhythm** · Languages: PHP → Python → TypeScript → Rust

## The problem

A slicer tells you a print needs 4.2 m of filament. Your scale tells you the
spool has 180 g left. Is that enough? To answer, Jig needs to convert between
**length** and **weight** of filament.

Filament is a long cylinder, so:

```text
cross-section area (mm²) = π × (diameter / 2)²
volume (mm³)             = area × length
volume (cm³)             = volume (mm³) / 1000
weight (g)               = volume (cm³) × density (g/cm³)
```

Typical densities: PLA ≈ 1.24 g/cm³, PETG ≈ 1.27 g/cm³. Check your filament
maker's data sheet for exact values.

**Sanity check you can do by hand:** 1 m of 1.75 mm PLA weighs about 3 g, so a
1 kg spool holds roughly 335 m.

## What you write

Two functions, in each language:

| Function | Takes | Returns |
| --- | --- | --- |
| `filament_grams` | length (mm), diameter (mm), density (g/cm³) | weight (g) |
| `filament_length_mm` | weight (g), diameter (mm), density (g/cm³) | length (mm) |

(TypeScript uses `filamentGrams` and `filamentLengthMm`, following its naming
convention.)

Ignore bad input such as negative lengths for now. Handling it is Lesson 05.

## How to work through it

Do the languages in order: PHP, then Python, then TypeScript, then Rust. For
each one:

1. **Red:** run the tests and watch them fail. Read the failure message.
   ```sh
   ./scripts/check 01 php
   ```
2. **Green:** open the stub file, replace the `TODO` with the simplest code
   that passes.
3. **Refactor:** with the tests passing, make the code clearer. Name the
   intermediate values. Remove repetition between the two functions. Run the
   tests again.
4. **Your test:** add one test of your own to the test file. Suggestion: TPU
   (density ≈ 1.21) or a 2.85 mm spool of PETG. Work out the expected value
   by hand *before* running it.

| Language | Stub you edit | Tests |
| --- | --- | --- |
| PHP | `php/filament.php` | `php/test.php` |
| Python | `python/filament.py` | `python/test_filament.py` |
| TypeScript | `ts/filament.ts` | `ts/filament.test.ts` |
| Rust | `rust/src/lib.rs` | `rust/tests/filament.rs` |

## What's different between the languages

Fill this in yourself as you go. Noticing differences is the point of writing
it four times. Prompts:

- **Number types:** PHP and Python have one float type. TypeScript has
  `number`. Rust makes you choose (`f64` here), and won't mix it with integers
  without an explicit conversion. What happens if you write `1000` instead of
  `1000.0` in Rust?
- **π:** where does each language keep it?
- **Comparing floats:** why do the tests check "close to" instead of `==`?
- **Where tests live:** the tests are a separate file in every language here.
  Idiomatic Rust often puts unit tests in the same file as the code. Why might
  that be useful?

## Done when

- [ ] `./scripts/check 01` passes in all four languages
- [ ] Each language has one test you wrote yourself
- [ ] You can explain the float-comparison question without looking it up

**Read alongside:** *The Rust Programming Language*, chapter 3 ("Common
Programming Concepts"): <https://doc.rust-lang.org/book/>
