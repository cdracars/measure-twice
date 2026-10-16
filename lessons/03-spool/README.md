# Lesson 03: Spool

**Stage 1 · Basics + TDD rhythm** · Languages: PHP · Python · TypeScript · Rust

## The problem

So far Jig has been loose functions taking loose numbers. Real code passes
around *things*. A **spool** is a thing: it has a material, a diameter, a
density, and an amount of filament left, and it changes as jobs use it up.

In this lesson you build a `Spool` type that keeps those values together and
protects them. Nothing outside the spool should be able to set its remaining
weight directly; the only way to use filament is through the spool's own
`consume` method.

## What you write

A `Spool` type, created with a material name, diameter (mm), density
(g/cm³), and grams remaining:

| Method | Returns | Notes |
| --- | --- | --- |
| `material` | the material name | |
| `grams_remaining` | grams left | read-only from outside |
| `remaining_length_mm` | length of filament left, in mm | lesson 01's formula |
| `can_print(grams)` | `true` if there's enough for a job of that weight | exactly enough counts |
| `consume(grams)` | nothing | uses up filament. Only call it after `can_print` says yes. |

Names follow each language's conventions:

| | PHP | Python | TypeScript | Rust |
| --- | --- | --- | --- | --- |
| Create | `new Spool('PLA', 1.75, 1.24, 1000.0)` | `Spool("PLA", 1.75, 1.24, 1000.0)` | `new Spool("PLA", 1.75, 1.24, 1000)` | `Spool::new("PLA", 1.75, 1.24, 1000.0)` |
| Methods | `gramsRemaining()`, `canPrint()` | `grams_remaining` (a property), `can_print()` | `gramsRemaining` (a getter), `canPrint()` | `grams_remaining()`, `can_print()` |

## New this lesson: you write all the tests for one method

`consume` has **no tests at all**. Write them yourself, before the code.
Things worth checking:

- Consuming reduces what's left by exactly that amount.
- Two jobs in a row add up.
- Consuming everything leaves zero, and `can_print` then refuses any job.
- The remaining length shrinks too.

What about consuming *more* than is left? The spec says callers must check
`can_print` first, so for now that case is undefined. That's a weak design:
a spec that relies on every caller remembering a rule. Lesson 05 fixes it.

## Encapsulation: how private is private?

Each language protects the remaining weight differently, and the differences
matter:

| | How to hide it | How hidden is it? |
| --- | --- | --- |
| PHP | `private` property, public getter | Enforced by the language |
| Python | `_grams_remaining` plus a read-only `@property` | A naming convention. Anyone *can* still write to `_grams_remaining` |
| TypeScript | `#gramsRemaining` (a JavaScript private field) plus a `get` accessor | Enforced at runtime. (TypeScript's `private` keyword only exists at compile time.) |
| Rust | Fields are private to their module by default; expose a method | Enforced by the compiler |

## How to work through it

Start with the language you know best, then the ones you're learning, with
your weakest last. For each language:

1. **Red:** `./scripts/check 03 rust` (or `php`, `python`, `ts`)
2. **Green:** fill in the constructor and methods until the given tests pass.
3. **Your tests:** write the `consume` tests, see them fail, then implement it.
4. **Refactor:** does `remaining_length_mm` repeat lesson 01's math? Could it
   be clearer?

| Language | Stub you edit | Tests |
| --- | --- | --- |
| PHP | `php/Spool.php` | `php/test.php` |
| Python | `python/spool.py` | `python/test_spool.py` |
| TypeScript | `ts/spool.ts` | `ts/spool.test.ts` |
| Rust | `rust/src/lib.rs` | `rust/tests/spool.rs` |

## What's different between the languages

| Question | PHP | Python | TypeScript | Rust |
| --- | --- | --- | --- | --- |
| What's the constructor called? | | | | |
| How does a method refer to its own object? | | | | |
| What must you write to change a field inside a method? | | | | |
| What must the *caller* write to be allowed to call `consume`? | | | | |
| Where are the fields declared? | | | | |

Hint for the last two rows in Rust: look at `&self` vs `&mut self`, and why
the tests say `let mut spool`.

Then answer in your own words:

- Rust makes you mark both the variable (`let mut`) and the method
  (`&mut self`) before anything can change. The other three let any method
  change any field. What kinds of bugs does Rust's rule prevent?

## Done when

- [ ] `./scripts/check 03` passes in all four languages
- [ ] You wrote every `consume` test, before implementing `consume`
- [ ] You can explain the difference between Python's `_grams_remaining` and
      PHP's `private`

**Read alongside:** *The Rust Programming Language*, chapter 5 ("Using
Structs to Structure Related Data"): <https://doc.rust-lang.org/book/>
