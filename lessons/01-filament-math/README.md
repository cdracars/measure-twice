# Lesson 01: Filament math

**Stage 1 · Basics + TDD rhythm** · Languages: PHP · Python · TypeScript · Rust

## What you're learning

**Test-driven development (TDD):** the tests come first. They describe what
the code must do, and you write code until they pass. A passing test is proof
you can re-check any time, whoever wrote the code: you, a teammate, or an AI.
It also tells you the moment a later change breaks something.

**The setup:** a teammate turned the filament maker's data sheet into tests,
and your job is to make them pass. Before any code, read what they wrote:
the tests are the spec, and [Reading the tests](#reading-the-tests) shows
how. The filament math is something concrete to practise on; the habit is the
point. In lesson 02 you swap roles and write the tests yourself.

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

## Reading the tests

Every test has the same three parts, whatever the language:

1. **A name** that says the behaviour in plain words: "one metre of 1.75 mm
   PLA weighs about 3 g".
2. **A call** to your function with some inputs: `filament_grams(1000.0, 1.75,
   1.24)` means 1000 mm of 1.75 mm filament with a density of 1.24.
3. **A check** that compares the answer with the expected value:
   `assert_close(2.98, …)` passes if the answer is within 0.01 of 2.98.
   Expected value first, your function's answer second.

That first test, in each language:

```php
// PHP: a tiny test runner at the top of php/test.php defines test().
test('one metre of 1.75 mm PLA weighs about 3 g', function () {
    assert_close(2.98, filament_grams(1000.0, 1.75, 1.24));
});
```

```python
# Python: unittest runs every method whose name starts with test_.
def test_one_metre_of_pla_weighs_about_3_g(self):
    self.assertAlmostEqual(2.98, filament_grams(1000.0, 1.75, 1.24), delta=0.01)
```

```ts
// TypeScript: test() comes from Node's built-in node:test.
test("one metre of 1.75 mm PLA weighs about 3 g", () => {
  assertClose(2.98, filamentGrams(1000, 1.75, 1.24));
});
```

```rust
// Rust: #[test] marks a function as a test; cargo test runs them all.
#[test]
fn one_metre_of_pla_weighs_about_3_g() {
    assert_close(2.98, filament_grams(1000.0, 1.75, 1.24), 0.01);
}
```

When a test fails, the guide shows its name and the check's message, such as
`expected 2.98 (± 0.01), got 0`. To write a test of your own later, copy one,
then change its name, inputs and expected value.

## How to work through it

Start with the language you know best, then do the ones you're learning, with
your weakest last. The first time through, you're working out the problem;
after that, you're learning how each language expresses the same answer.

Running `./scripts/guide`? It runs the tests for you and takes you through
these steps one at a time: edit the stub, save, and watch the terminal.
Without the guide, for each language:

0. **Read the tests:** find the first test in the tests file and work out its
   expected answer by hand with the formula above. Now you know what the code
   must do before you write any.
1. **Red:** run the tests and watch them fail. Read the failure message.
   ```sh
   ./scripts/check 01 rust     # or php, python, ts
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

| Question | PHP | Python | TypeScript | Rust |
| --- | --- | --- | --- | --- |
| What number type holds `1.75`? | | | | |
| Can you write `1000` where a float is expected? | | | | |
| Where does π live? | | | | |
| What happens when an unfinished stub runs? | | | | |
| Where do tests usually live: same file or separate? | | | | |

Then answer in your own words:

- Which languages let you mix integers and floats freely, and which make you
  convert? What does each choice protect you from, or cost you?
- Why do the tests check "close to" instead of `==`? Does that apply in all
  four languages?

## Done when

- [ ] `./scripts/check 01` passes in all four languages
- [ ] Each language has one test you wrote yourself
- [ ] You can explain the float-comparison question without looking it up

**Read alongside:** *The Rust Programming Language*, chapter 3 ("Common
Programming Concepts"): <https://doc.rust-lang.org/book/>
