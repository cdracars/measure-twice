use lesson_09_jig::{Output, USAGE, run};

fn stdout(code: i32, text: &str) -> Output {
    Output {
        code,
        stdout: text.to_string(),
        stderr: String::new(),
    }
}

fn stderr(code: i32, text: &str) -> Output {
    Output {
        code,
        stdout: String::new(),
        stderr: text.to_string(),
    }
}

// help and errors

#[test]
fn help_prints_the_usage() {
    assert_eq!(run(&["help"]), stdout(0, USAGE));
}

#[test]
fn no_arguments_prints_the_usage_as_an_error() {
    assert_eq!(run(&[]), stderr(2, USAGE));
}

#[test]
fn an_unknown_command_is_an_error() {
    assert_eq!(
        run(&["frobnicate"]),
        stderr(
            2,
            "jig: unknown command: frobnicate\nrun 'jig help' to see the commands\n"
        )
    );
}

// grams

#[test]
fn grams_of_pla() {
    assert_eq!(run(&["grams", "1000", "PLA"]), stdout(0, "2.98 g\n"));
}

#[test]
fn grams_accepts_a_lowercase_material() {
    assert_eq!(run(&["grams", "4200", "petg"]), stdout(0, "12.83 g\n"));
}

#[test]
fn grams_rejects_a_bad_length() {
    assert_eq!(
        run(&["grams", "abc", "PLA"]),
        stderr(2, "jig: not a length: abc\n")
    );
}

#[test]
fn grams_rejects_an_unknown_material() {
    assert_eq!(
        run(&["grams", "1000", "Nylon"]),
        stderr(2, "jig: unknown material: Nylon\n")
    );
}

#[test]
fn grams_needs_exactly_two_arguments() {
    assert_eq!(
        run(&["grams", "1000"]),
        stderr(2, "jig: usage: jig grams <length-mm> <material>\n")
    );
}

// check

#[test]
fn check_a_good_temperature() {
    assert_eq!(
        run(&["check", "PLA", "205"]),
        stdout(0, "ok: PLA prints at 190–220 °C\n")
    );
}

#[test]
fn check_a_cold_temperature() {
    assert_eq!(
        run(&["check", "petg", "200"]),
        stdout(1, "too cold: PETG prints at 220–250 °C\n")
    );
}

#[test]
fn check_a_hot_temperature() {
    assert_eq!(
        run(&["check", "TPU", "240"]),
        stdout(1, "too hot: TPU prints at 210–230 °C\n")
    );
}

#[test]
fn check_rejects_a_bad_temperature() {
    assert_eq!(
        run(&["check", "PLA", "hot"]),
        stderr(2, "jig: not a temperature: hot\n")
    );
}

#[test]
fn check_needs_exactly_two_arguments() {
    assert_eq!(
        run(&["check", "PLA", "205", "extra"]),
        stderr(2, "jig: usage: jig check <material> <nozzle-c>\n")
    );
}

// log: no tests yet. Write them before the code.
