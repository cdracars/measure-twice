# Lesson 02: Nozzle temperature

**Stage 1 · Basics + TDD rhythm** · Languages: PHP · Python · TypeScript · Rust

## What you're learning

Writing tests yourself, before the code, and choosing inputs that catch bugs.

**The setup:** you swap roles. In lesson 01 a teammate wrote the tests and you
made them pass. `nozzle_verdict` still comes with their tests, but
`needs_enclosure` comes with just one, and you write the rest before its code.
This back-and-forth, where one person writes a failing test and the other makes
it pass, is called **ping-pong pairing**. You don't need a partner: here you
play both sides.

You also meet **boundary values**: the inputs at the very edge of a range,
where bugs cluster. Both are how you check code you didn't write, including
code an AI wrote.

## The problem

Before Jig starts a print job, it should catch obvious mistakes, such as
printing PETG at a PLA temperature. Each material has a range of nozzle
temperatures that usually works. Outside it, the plastic doesn't melt
properly (too cold) or degrades and strings (too hot).

Jig's starting ranges, in °C:

| Material | Min | Max |
| --- | --- | --- |
| PLA | 190 | 220 |
| PETG | 220 | 250 |
| ABS | 230 | 260 |
| TPU | 210 | 230 |

These are typical starting points, not universal truths. Every filament maker
prints its own range on the spool. For this lesson, the table is the spec.

Some materials also want an **enclosure**, a box around the printer that
keeps warm air in. ABS shrinks as it cools, and drafts make it warp and
crack. Of the four materials above, only ABS needs an enclosure.

## What you write

| Function | Takes | Returns |
| --- | --- | --- |
| `nozzle_verdict` | material name, nozzle temperature (°C, whole number) | `"too cold"`, `"ok"`, `"too hot"`, or `"unknown material"` |
| `needs_enclosure` | material name | `true` or `false` (unknown materials: `false`) |

(TypeScript: `nozzleVerdict` and `needsEnclosure`.)

Material names are exact: `"PLA"`, not `"pla"`. Both ends of each range count
as `"ok"`.

## New this lesson: you write some of the tests

`nozzle_verdict` comes with tests, as in lesson 01. `needs_enclosure` comes
with **one** example test. Before you write any of its code:

1. Write the rest of its tests. Ask: what inputs could the code get wrong?
   Cover every material in the table, plus one that isn't in it.
2. Run them and watch them fail.
3. Then write the code.

If your tests all pass before you've written the code, they aren't testing
anything. That's the reason for watching them fail first.

## Boundary values

Look at the `nozzle_verdict` tests. Most of them sit right at the edge of a
range: 190 and 189, 220 and 221. Bugs cluster at boundaries: `<` where you
meant `<=`, or a range off by one. Testing the middle of a range (205) finds
almost nothing that testing 190, 189, 220 and 221 wouldn't.

When you write your own tests from now on, ask where the boundaries are.

## How to work through it

Start with the language you know best, then do the ones you're learning, with
your weakest last.

The guide takes you through this one step at a time: make the
`nozzle_verdict` tests pass, write the `needs_enclosure` tests and watch them
fail, make them pass, then refactor. It re-runs the tests every time you save,
and it only counts your `needs_enclosure` tests once it has seen them fail. In
a codespace it's already running in the terminal; anywhere else, start it
with `./scripts/guide`.

| Language | Stub you edit | Tests |
| --- | --- | --- |
| PHP | `php/temperature.php` | `php/test.php` |
| Python | `python/temperature.py` | `python/test_temperature.py` |
| TypeScript | `ts/temperature.ts` | `ts/temperature.test.ts` |
| Rust | `rust/src/lib.rs` | `rust/tests/temperature.rs` |

<details>
<summary>Working without the guide</summary>

The same steps by hand, for each language:

1. **Red:** `./scripts/check 02 rust` (or `php`, `python`, `ts`)
2. **Green:** make the `nozzle_verdict` tests pass.
3. **Your tests:** write the `needs_enclosure` tests, see them fail, then make
   them pass.
4. **Refactor:** with everything green, make it clearer.

</details>

## What's different between the languages

All four languages have a way to choose between several cases, but they
behave very differently:

| Question | PHP | Python | TypeScript | Rust |
| --- | --- | --- | --- | --- |
| What's the multi-way branch called? | | | | |
| Is it an expression (gives a value) or a statement? | | | | |
| What happens if no case matches? | | | | |
| Does it fall through to the next case if you forget something? | | | | |
| Does the compiler or interpreter check you covered every case? | | | | |

Hints for finding out: PHP 8 has both `switch` and `match`. Python 3.10 added
`match`. TypeScript has `switch`. In Rust, try deleting the `_` arm of your
`match` and read the compiler error.

Then answer in your own words:

- The verdicts are plain strings. What happens if a caller checks for
  `"too_cold"` instead of `"too cold"`? Which of the four languages would
  catch that mistake, and when? (Lesson 04 fixes this with enums.)

## Done when

- [ ] The guide has taken you through lesson 02 in every language you chose
  (without the guide: `./scripts/check 02` passes in each of them)
- [ ] You wrote the `needs_enclosure` tests before its code, in each language
- [ ] You can explain why the tests use 189, 190, 220 and 221 rather than 205

**Read alongside:** *The Rust Programming Language*, chapter 3.5 ("Control
Flow") and chapter 6.2 ("The `match` Control Flow Construct"):
<https://doc.rust-lang.org/book/>
