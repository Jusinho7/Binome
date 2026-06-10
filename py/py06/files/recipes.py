# Absolute import: uses full path from project root
from alchemy.elements import create_air
# Relative import: uses position within the package
from ..potions import strength_potion
from elements import create_fire


def lead_to_gold() -> str:
    """Return a transmutation recipe string."""
    return (
        f"Recipe transmuting Lead to Gold: brew '{create_air()}'"
        f" and '{strength_potion()}'"
        f" mixed with '{create_fire()}'"
    )
