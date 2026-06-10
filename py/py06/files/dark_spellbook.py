from .dark_validator import validate_dark_ingredients


def dark_spell_allowed_ingredients() -> list[str]:
    """Return allowed ingredients for dark magic."""
    return ["bats", "frogs", "arsenic", "eyeball"]


def dark_spell_record(spell_name: str, ingredients: str) -> str:
    """Record or reject a dark spell based on ingredient validation."""
    result = validate_dark_ingredients(ingredients)
    if "VALID" in result and "INVALID" not in result:
        return f"Dark spell recorded: {spell_name} ({result})"
    return f"Dark spell rejected: {spell_name} ({result})"
