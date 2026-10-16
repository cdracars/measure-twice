# Lesson 04: Material

**Stage 1 · Basics + TDD rhythm** · Languages: PHP · Python · TypeScript · Rust

## The problem

Lesson 02 passed materials around as strings, and returned verdicts as
strings too. That caused two kinds of bugs, and you probably met both:

- A caller could ask about `"pla"` or `"Nylon"`, so every function needed an
  `"unknown material"` case.
- A caller checking for `"too_cold"` instead of `"too cold"` would silently
  never match.

An **enum** is a type with a fixed list of possible values. If `Material` can
only be PLA, PETG, ABS, or TPU, there is no unknown material to handle: the
bad value can't be created in the first place. That idea, *make invalid
states impossible to represent*, comes back throughout the course.

## What you write

A `Material` type with exactly four values, and a `Verdict` type with exactly
three (too cold, OK, too hot). Then:

| Function | Returns | Values |
| --- | --- | --- |
| density | g/cm³ | PLA 1.24, PETG 1.27, ABS 1.04, TPU 1.21 |
| nozzle range | (min °C, max °C) | Same as lesson 02: PLA 190–220, PETG 220–250, ABS 230–260, TPU 210–230 |
| needs enclosure | `true` / `false` | Only ABS |
| nozzle verdict | a `Verdict` | Both ends of the range count as OK |

The densities and temperatures are typical starting values. Check your
filament maker's data sheet for real prints.

How each language spells it:

| | PHP | Python | TypeScript | Rust |
| --- | --- | --- | --- | --- |
| Material values | `Material::PLA` | `Material.PLA` | `"PLA"` | `Material::Pla` |
| Verdict values | `Verdict::TooCold` | `Verdict.TOO_COLD` | `"too cold"` | `Verdict::TooCold` |
| Methods | `$m->density()`, `$m->nozzleRange()`, `$m->needsEnclosure()` | `m.density()`, `m.nozzle_range()`, `m.needs_enclosure()` | functions: `density(m)`, `nozzleRange(m)`, `needsEnclosure(m)` | `m.density()`, `m.nozzle_range()`, `m.needs_enclosure()` |
| Verdict | `nozzle_verdict($m, $c)` | `nozzle_verdict(m, c)` | `nozzleVerdict(m, c)` | `nozzle_verdict(m, c)` |
| Every material | `Material::cases()` | `list(Material)` | `MATERIALS` | `Material::ALL` |

### Why TypeScript looks different

TypeScript has an `enum` keyword, but this course runs TypeScript directly in
Node, which only *strips* types and can't run `enum` (it generates code). Most
modern TypeScript uses a **union of string literals** instead:

```ts
type Verdict = "too cold" | "ok" | "too hot";
```

That's still a closed set: `nozzleVerdict` can't return `"too_cold"`, because
the type checker rejects it. Run `npm run typecheck` to see that safety; the
tests alone won't show it.

## New this lesson: port your boundary tests

`nozzle_verdict` comes with one example test. Write the rest yourself. You
did this thinking in lesson 02: where are the boundaries? Cover them for at
least two materials.

Notice what you *don't* need to test any more: unknown materials.

## How to work through it

Start with the language you know best, then the ones you're learning, with
your weakest last.

1. **Red:** `./scripts/check 04 rust` (or `php`, `python`, `ts`)
2. **Green:** implement density, nozzle range, and needs enclosure.
3. **Your tests:** write the `nozzle_verdict` boundary tests, see them fail,
   then implement it.
4. **Refactor:** can `nozzle_verdict` reuse the nozzle range method?

| Language | Stub you edit | Tests |
| --- | --- | --- |
| PHP | `php/material.php` | `php/test.php` |
| Python | `python/material.py` | `python/test_material.py` |
| TypeScript | `ts/material.ts` | `ts/material.test.ts` |
| Rust | `rust/src/lib.rs` | `rust/tests/material.rs` |

## What's different between the languages

| Question | PHP | Python | TypeScript | Rust |
| --- | --- | --- | --- | --- |
| Can an enum value carry methods? | | | | |
| If you add a fifth material and forget to update `density`, when do you find out? | | | | |
| Can you get a list of every value? | | | | |
| Can you compare two values with `==` / `===`? | | | | |

Try the second row for real: add `NYLON` (or `Nylon`) to `Material` in each
language without updating anything else, and run the type checker, the
compiler, and the tests. Write down which one tells you first. Then undo it.

Then answer in your own words:

- Where did lesson 02's `"unknown material"` case go? What does that do to
  the number of tests you need?
- Rust's compiler checks every `match` covers every case. TypeScript can do
  the same with a `never` check in the `default` branch. Look it up: how does
  it work?

## Done when

- [ ] `./scripts/check 04` passes in all four languages
- [ ] `npm run typecheck` passes
- [ ] You wrote boundary tests for `nozzle_verdict` in each language
- [ ] You can explain how an enum removes the need for an "unknown" case

**Read alongside:** *The Rust Programming Language*, chapter 6 ("Enums and
Pattern Matching"): <https://doc.rust-lang.org/book/>
