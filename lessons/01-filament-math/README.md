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

You don't need to type π in yourself: all four languages have it built in, as
a constant more precise than 3.14159. Finding where each one keeps it is a row
in [the comparison table](#whats-different-between-the-languages), and the
guide's hints name it if you get stuck.

## Reading the tests

Every test has the same three parts, whatever the language:

1. **A name** that says the behaviour in plain words: "one metre of 1.75 mm
   PLA weighs about 3 g".
2. **A call** to the function you'll write, with some inputs: `filament_grams(1000.0, 1.75,
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

## Worked example

The first test says one metre (1000 mm) of 1.75 mm PLA, density 1.24 g/cm³,
weighs 2.98 g. Here's where that number comes from. Grab a calculator and
follow along.

**1. Find the radius.** The diameter, 1.75 mm, is how wide the filament is,
straight across. The radius is half of that: from the middle to the edge.

```text
radius = 1.75 ÷ 2 = 0.875 mm
```

**2. Find the area of the end.** Cut the filament and look at the cut end: it's
a circle. A circle's area is π × radius × radius, where π ≈ 3.14159. The answer
is in mm² (square millimetres) because you multiplied millimetres by
millimetres.

```text
area = 3.14159 × 0.875 × 0.875 ≈ 2.405 mm²
```

**3. Find the volume.** A length of filament is that circle stretched out, like
a stack of very thin slices. Area × length is how much space the whole piece
fills, in mm³ (cubic millimetres).

```text
volume = 2.405 × 1000 ≈ 2405 mm³
```

**4. Change mm³ to cm³.** Density is given per cm³, so the volume has to be in
cm³ too. 1 cm is 10 mm, so a 1 cm cube is 10 × 10 × 10 = 1000 mm³. Divide by
1000.

```text
volume = 2405 ÷ 1000 ≈ 2.405 cm³
```

**5. Find the weight.** Density says how much each cm³ weighs: PLA weighs
1.24 g per cm³. Multiply the volume by it.

```text
weight = 2.405 × 1.24 ≈ 2.98 g   ← the test's expected value
```

All five steps together, which is the formula from "The problem" with real
numbers in it:

```text
radius       = 1.75 ÷ 2        = 0.875 mm
area         = π × 0.875²      ≈ 2.405 mm²
volume (mm³) = 2.405 × 1000    ≈ 2405 mm³
volume (cm³) = 2405 ÷ 1000     ≈ 2.405 cm³
weight       = 2.405 × 1.24    ≈ 2.98 g
```

So 1 m of 1.75 mm PLA weighs about 3 g, and a 1 kg spool holds roughly
1000 ÷ 2.98 ≈ 335 m. The test's expected value came from the spec, worked out
before any code existed. That's what makes it a fair check of the code.

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

Start with the language you know best, then do the ones you're learning, with
your weakest last. The first time through, you're working out the problem;
after that, you're learning how each language expresses the same answer.

The guide takes you through this one step at a time: read your teammate's
tests, make them pass, refactor, then add a test of your own. It re-runs the
tests every time you save and tells you what to do next. In a codespace, the
Measure Twice panel in the sidebar takes you through it, with the guide
running in a terminal behind it; anywhere else, start it with
`./scripts/guide`.

| Language | Stub you edit | Tests |
| --- | --- | --- |
| PHP | `php/filament.php` | `php/test.php` |
| Python | `python/filament.py` | `python/test_filament.py` |
| TypeScript | `ts/filament.ts` | `ts/filament.test.ts` |
| Rust | `rust/src/lib.rs` | `rust/tests/filament.rs` |

<details>
<summary>Working without the guide</summary>

The same steps by hand, for each language:

0. **Read the tests:** find the first test in the tests file, then follow the
   [worked example](#worked-example) and see that it ends at the same 2.98 g.
   Now you know what the code must do before you write any.
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
   by hand *before* running it, the same way as the worked example.

</details>

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

- [ ] The guide has taken you through lesson 01 in every language you chose
  (without the guide: `./scripts/check 01` passes in each of them)
- [ ] Each language has one test you wrote yourself
- [ ] You can explain the float-comparison question without looking it up

**Read alongside:** *The Rust Programming Language*, chapter 3 ("Common
Programming Concepts"): <https://doc.rust-lang.org/book/>
