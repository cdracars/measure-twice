# Glossary

The shared vocabulary for Jig and for this course. When code, tests, and docs
use the same words for the same things, the code gets easier to read. That's
the first idea of domain modeling. Add terms as lessons introduce them.

## Workshop (Jig's domain)

**Build Log**
: Dated record of what happened in the workshop: prints, failures, repairs,
  changes. Entries are tied to a project.

**Density**
: Mass per volume of a material, in g/cm³. Used to convert filament length to
  weight. PLA is about 1.24, PETG about 1.27.

**FDM (fused deposition modeling)**
: 3D printing by melting plastic **filament** and laying it down layer by
  layer. Jig's first kind of **machine**.

**Filament**
: Plastic wire fed into an FDM printer, sold on **spools**. Common diameters:
  1.75 mm and 2.85 mm.

**G-code**
: The text instructions a printer executes. **Slicers** write estimates such
  as filament used and print time into it as comments.

**Job**
: One piece of work on one **machine**, such as a single print. Moves through
  states: queued, running, done, failed, cancelled.

**Machine**
: Equipment that runs **jobs**: an FDM printer, later a laser cutter or CNC
  router.

**Material**
: What a job uses up: filament, sheet stock, and so on.

**Slicer**
: Software that turns a 3D model into **G-code** for a specific printer.

**Spool**
: A reel of filament with a material, a diameter, and an amount remaining.

## Course

**ADR (architecture decision record)**
: A short document recording one decision, its context, and its
  consequences. Lives in `docs/adr/`.

**Red, green, refactor**
: The TDD loop. Red: a failing test. Green: the simplest code that passes.
  Refactor: improve the code while the tests stay green.

**Stub**
: A function with the right name and signature whose body is a `TODO`. You
  replace the body.

**TDD (test-driven development)**
: Writing a failing test before the code that makes it pass.
