use lesson_05_bad_input::{
    GramsError, Material, NotEnoughFilament, Spool, UnknownMaterial, parse_grams, parse_material,
};

#[test]
fn parse_grams_accepts() {
    let cases = [
        ("250", 250.0),
        ("12.5", 12.5),
        ("12.5 g", 12.5),
        ("40g", 40.0),
        (" 40g ", 40.0),
        ("0", 0.0),
    ];
    for (text, grams) in cases {
        assert_eq!(parse_grams(text), Ok(grams), "{text:?}");
    }
}

#[test]
fn parse_grams_rejects() {
    let cases = [
        ("", GramsError::Empty),
        ("   ", GramsError::Empty),
        ("abc", GramsError::NotANumber),
        ("12.5 kg", GramsError::NotANumber),
        ("nan", GramsError::NotANumber),
        ("inf", GramsError::NotANumber),
        ("0x10", GramsError::NotANumber),
        ("1_000", GramsError::NotANumber),
        ("-5", GramsError::Negative),
        ("-5 g", GramsError::Negative),
    ];
    for (text, error) in cases {
        assert_eq!(parse_grams(text), Err(error), "{text:?}");
    }
}

#[test]
fn consuming_what_is_available_works() {
    let mut spool = Spool::new(100.0);
    assert_eq!(spool.consume(40.0), Ok(()));
    assert_eq!(spool.grams_remaining(), 60.0);
}

#[test]
fn consuming_exactly_what_is_left_works() {
    let mut spool = Spool::new(100.0);
    assert_eq!(spool.consume(100.0), Ok(()));
    assert_eq!(spool.grams_remaining(), 0.0);
}

#[test]
fn consuming_more_than_is_left_is_refused() {
    let mut spool = Spool::new(100.0);
    assert_eq!(
        spool.consume(100.5),
        Err(NotEnoughFilament {
            needed: 100.5,
            remaining: 100.0
        })
    );
}

#[test]
fn a_refused_consume_leaves_the_spool_unchanged() {
    let mut spool = Spool::new(100.0);
    let _ = spool.consume(150.0);
    assert_eq!(spool.grams_remaining(), 100.0);
}

// parse_material: one example. Write the rest before the code.

#[test]
fn parse_material_accepts_pla() {
    assert_eq!(parse_material("PLA"), Ok(Material::Pla));
}

#[test]
fn parse_material_ignores_case() {
    assert_eq!(parse_material("petg"), Ok(Material::Petg));
    assert_eq!(parse_material("Tpu"), Ok(Material::Tpu));
}

#[test]
fn parse_material_ignores_surrounding_spaces() {
    assert_eq!(parse_material("  ABS "), Ok(Material::Abs));
}

#[test]
fn parse_material_rejects_an_unknown_material() {
    assert_eq!(
        parse_material("Nylon"),
        Err(UnknownMaterial("Nylon".to_string()))
    );
}

#[test]
fn parse_material_rejects_empty_input() {
    assert!(parse_material("").is_err());
}
