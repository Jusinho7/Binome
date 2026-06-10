def validate_ingredients(ingredients: str) -> str:
    """Validate ingredients against allowed list from spellbook."""
    # Lazy import inside function to break the circular dependency
    from alchemy.grimoire.light_spellbook import (
        light_spell_allowed_ingredients,
    )
    allowed = light_spell_allowed_ingredients()
    ingredients_lower = ingredients.lower()
    for item in allowed:
        if item in ingredients_lower:
            return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
