from .dark_validator import validate_dark_ingredients


def dark_spell_allowed_ingredients() -> list[str]:
    return ["bats", "frogs", "arsenic", "eyeball"]


def dark_spell_record(spell_name: str, ingredients: str) -> str:
    result = validate_dark_ingredients(ingredients)
    if "VALID" in result and "INVALID" not in result:
        return f"Dark spell recorded: {spell_name} ({result})"
    return f"Dark spell rejected: {spell_name} ({result})"
