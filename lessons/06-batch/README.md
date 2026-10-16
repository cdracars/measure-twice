# Lesson 06: Batch

**Stage 1 · Basics + TDD rhythm** · Languages: PHP · Python · TypeScript · Rust

## The problem

A Friday print queue might hold a dozen **jobs**: a Benchy to test a new
spool, some brackets, a vase. Before starting, you want answers about the
whole batch: how much filament in total, how much of each material, which
job is the biggest, and which jobs use PLA.

That means working with collections: lists of jobs, and maps from material to
grams.

## What you write

A `Job` has a name, a material, and a weight in grams. It's already declared
in each stub file. You write:

| Function | Returns |
| --- | --- |
| `total_grams(jobs)` | the sum of every job's grams (0 for no jobs) |
| `grams_by_material(jobs)` | a map from material to total grams, with only the materials that appear |
| `heaviest_job(jobs)` | the job with the most grams, or nothing if there are no jobs. If several tie, the **first** one wins. |
| `jobs_using(jobs, material)` | the names of the jobs using that material, in their original order |

(TypeScript: `totalGrams`, `gramsByMaterial`, `heaviestJob`, `jobsUsing`.)

"Nothing" for `heaviest_job` is spelled differently in each language:
`null` in PHP, `None` in Python, `undefined` in TypeScript, and `None` (an
`Option`) in Rust.

## Loops or pipelines?

Every function here can be written two ways:

```text
loop:      total = 0; for each job: total += job.grams
pipeline:  jobs → map to grams → sum
```

Try both, in at least one language. Neither is always better: pipelines say
*what* you want, loops make every step explicit. Notice which one you find
easier to read a week later.

| | Loop | Pipeline |
| --- | --- | --- |
| PHP | `foreach` | `array_map`, `array_filter`, `array_sum` |
| Python | `for` | comprehensions, `sum()`, `max()` |
| TypeScript | `for...of` | `.map()`, `.filter()`, `.reduce()` |
| Rust | `for` | `.iter().map()`, `.filter()`, `.sum()` |

## Two traps, checked on this course's toolchain

**Ties.** "If several tie, the first one wins" sounds like what `max` does.
In Python, it is: `max()` returns the first of several equal items. In Rust,
`Iterator::max_by` returns the **last** one. Both are documented behaviour,
and a test that only uses distinct weights will never notice the difference.

**Enum keys in PHP.** PHP arrays can't use an enum case as a key:
`[Material::PLA => 1.0]` throws a `TypeError`. The PHP version of
`grams_by_material` therefore returns an array keyed by the material's string
value (`'PLA'`), which is what `Material::PLA->value` gives you.

## New this lesson: you choose which cases to test

`heaviest_job` comes with one example test. Its rules have two cases that are
easy to get wrong: what are they? Write tests for both before you write the
code. (Hint: re-read the table above.)

## How to work through it

Start with the language you know best, then the ones you're learning, with
your weakest last.

1. **Red:** `./scripts/check 06 rust` (or `php`, `python`, `ts`)
2. **Green:** `total_grams`, `grams_by_material`, `jobs_using`.
3. **Your tests:** write the `heaviest_job` tests, see them fail, then
   implement it.
4. **Refactor:** rewrite one function in the other style (loop ↔ pipeline).
   The tests tell you whether you broke it.

| Language | Stub you edit | Tests |
| --- | --- | --- |
| PHP | `php/batch.php` | `php/test.php` |
| Python | `python/batch.py` | `python/test_batch.py` |
| TypeScript | `ts/batch.ts` | `ts/batch.test.ts` |
| Rust | `rust/src/lib.rs` | `rust/tests/batch.rs` |

## What's different between the languages

| Question | PHP | Python | TypeScript | Rust |
| --- | --- | --- | --- | --- |
| What's the list type called? | | | | |
| What's the map / dictionary type called? | | | | |
| How do you represent "no value"? | | | | |
| Does `heaviest_job` return a copy of the job, or the original? | | | | |
| What does the compiler or type checker make you do before using the result of `heaviest_job`? | | | | |

Then answer in your own words:

- In Rust, `heaviest_job` returns `Option<&Job>`: a *reference* to a job
  inside the list you passed in. What would happen if the list were freed
  while you still held that reference? Why can't that happen in Rust?

## Done when

- [ ] `./scripts/check 06` passes in all four languages
- [ ] You wrote `heaviest_job` tests for both tricky cases, in each language
- [ ] You rewrote at least one function in the other style, with tests green

**Read alongside:** *The Rust Programming Language*, chapter 8 ("Common
Collections") and chapter 13.2 ("Processing a Series of Items with
Iterators"): <https://doc.rust-lang.org/book/>
