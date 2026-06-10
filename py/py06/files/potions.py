from alchemy.elements import create_earth, create_air
from elements import create_fire, create_water


def healing_potion() -> str:
    """Return a healing potion string using earth and air elements."""
    return (
        f"Healing potion brewed with '{create_earth()}'"
        f" and '{create_air()}'"
    )


def strength_potion() -> str:
    """Return a strength potion string using fire and water elements."""
    return (
        f"Strength potion brewed with '{create_fire()}'"
        f" and '{create_water()}'"
    )
