//! The entry point: the only code that touches the real terminal. Given.

use std::io::Write;
use std::process::ExitCode;

fn main() -> ExitCode {
    // The first argument is the program's own name; skip it.
    let args: Vec<String> = std::env::args().skip(1).collect();
    let args: Vec<&str> = args.iter().map(String::as_str).collect();

    let output = lesson_09_jig::run(&args);
    // If printing fails (say, the output pipe was closed), there's nothing
    // useful left to do, so the errors are ignored.
    let _ = std::io::stdout().write_all(output.stdout.as_bytes());
    let _ = std::io::stderr().write_all(output.stderr.as_bytes());
    ExitCode::from(u8::try_from(output.code).unwrap_or(1))
}
