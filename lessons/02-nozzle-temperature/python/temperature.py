def nozzle_verdict(material: str, nozzle_c: int) -> str:
    """Whether a nozzle temperature suits a material:
    "too cold", "ok", "too hot", or "unknown material"."""
    match material:
        case "PLA":
            low, high = 190, 220
        case "PETG":
            low, high = 220, 250
        case "ABS":
            low, high = 230, 260
        case "TPU":
            low, high = 210, 230
        case _:
            return "unknown material"

    if nozzle_c < low:
        return "too cold"
    if nozzle_c > high:
        return "too hot"
    return "ok"


def needs_enclosure(material: str) -> bool:
    """Whether a material needs an enclosed printer."""
    return material == "ABS"
