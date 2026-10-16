# Lesson 10: Test frameworks

**Stage 2 opener** · Languages: PHP · Python · TypeScript · Rust

## The problem

Every stage 1 test ran on a tiny hand-written helper: a `test()` function, an
`assert_close()`, a counter of failures. That kept setup simple, and it showed
there's no magic in a test: it's code that runs other code and complains.

Real projects use test frameworks. From here on, so does this course
([ADR 0003](../../docs/adr/0003-realistic-tools-from-stage-2.md)). In this
lesson nothing new gets built. Lesson 01's filament math is given, finished,
and you move its tests onto each language's standard framework, to see what a
framework adds over the helpers you've been using.

## Setup

Stage 2 needs a little more installed than stage 1:

| Language | Needs | Install | Then |
| --- | --- | --- | --- |
| PHP | PHP 8.4.1+, Composer | <https://getcomposer.org/download/> | `scripts/check` runs `composer install` for you |
| Python | uv | <https://docs.astral.sh/uv/getting-started/installation/> | `uv run` installs pytest on first use |
| TypeScript | nothing new | | `npm install` in the repository root |
| Rust | nothing new | | `cargo test` is already the framework |

If your `php` command is an older version but you have 8.4 installed under
another name, tell the check script: `PHP=php8.4 ./scripts/check 10 php`.

## What you write

Port all six of lesson 01's tests to each framework. Each file has one test
already ported as an example. Use the framework's features rather than
copying the stage 1 helpers across:

| | Approximate comparison | Many cases, one test | Run one test by name |
| --- | --- | --- | --- |
| PHPUnit | `assertEqualsWithDelta($expected, $actual, $delta)` | `#[DataProvider('cases')]` | `vendor/bin/phpunit --filter metre` |
| pytest | `assert actual == pytest.approx(expected, abs=0.01)` | `@pytest.mark.parametrize` | `uv run pytest -k metre` |
| Vitest | `expect(actual).toBeCloseTo(expected, digits)` | `it.each([...])` | `npx vitest run -t metre` |
| Rust | your own `assert_close` (Rust's standard library has no float assertion) | a loop over a table, or one test per case | `cargo test metre` |

Then, for Rust only, two things the other three don't have:

- **Unit tests in the same file.** Stage 1 put Rust tests in `tests/`, where
  they see only the public API. Here they live in a `#[cfg(test)] mod tests`
  inside `src/lib.rs`, so they can also test the private `grams_per_mm`. Add
  one test that does.
- **Doc tests.** Add an `# Examples` section to `filament_grams`'s
  documentation with a short example. `cargo test` compiles and runs it, so the
  example in the docs can't quietly go stale.

| Language | Code (given) | Tests you write |
| --- | --- | --- |
| PHP | `php/src/filament.php` | `php/tests/FilamentTest.php` |
| Python | `python/filament.py` | `python/test_filament.py` |
| TypeScript | `ts/filament.ts` | `ts/filament.test.ts` |
| Rust | `rust/src/lib.rs` | the `tests` module and doc comment in `rust/src/lib.rs` |

## Red, without writing new code

The code already works, so the tests pass as soon as you write them. Before
trusting a passing test, make it fail on purpose:

1. Write a test and run it: green.
2. Break the code it covers. Change `1000` to `100` in `grams_per_mm`, or
   swap `*` for `/`.
3. Run again. The test should go red. **Read the failure output.**
4. Undo the change.

A test you have never seen fail might not be testing anything. Breaking code
on purpose to check the tests notice is the idea behind *mutation testing*,
which stage 5 automates.

## What does the framework add?

Compare a stage 1 failure with a framework failure for the same broken code:

| Question | PHP | Python | TypeScript | Rust |
| --- | --- | --- | --- | --- |
| Does the failure show expected and actual values? | | | | |
| Does it show the line of the failing assertion? | | | | |
| How does it find tests? (file names, function names, attributes?) | | | | |
| How does a parametrized case show up when one case fails? | | | | |

Then answer in your own words:

- pytest uses plain `assert` and still shows both values when it fails. The
  other three need special assertion functions. How does pytest manage it?
  (Look up "pytest assertion rewriting".)
- What did you give up by moving off the stage 1 helpers? Was it worth it?

## Done when

- [ ] All six lesson 01 tests ported in each language, using parametrization
      where cases repeat
- [ ] You saw every test fail at least once by breaking the code on purpose
- [ ] Rust has a unit test of `grams_per_mm` and a doc test on `filament_grams`
- [ ] `./scripts/check 10` passes

**Read alongside:** *The Rust Programming Language*, chapter 11 ("Writing
Automated Tests"): <https://doc.rust-lang.org/book/>
