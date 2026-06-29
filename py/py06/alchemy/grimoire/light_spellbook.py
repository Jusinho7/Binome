def light_spell_allowed_ingredients() -> list[str]:
    return ["earth", "air", "fire", "water"]


def light_spell_record(spell_name: str, ingredients: str) -> str:
    from .light_validator import validate_ingredients
    result = validate_ingredients(ingredients)
    if "VALID" in result:
        return f"Light spell recorded: {spell_name} ({result})"
    else:
        return f"Ligth spell rejected: {spell_name} ({result})"
