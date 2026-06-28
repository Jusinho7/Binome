from ex0.creature import Creature


class Flameling(Creature):
    """Base fire-type Creature."""

    def __init__(self) -> None:
        super().__init__("Flameling", "Fire")

    def attack(self) -> str:
        return f"{self._name} uses Ember!"


class Pyrodon(Creature):
    """Evolved fire/flying-type Creature."""

    def __init__(self) -> None:
        super().__init__("Pyrodon", "Fire/Flying")

    def attack(self) -> str:
        return f"{self._name} uses Flamethrower!"


class Aquabub(Creature):
    """Base water-type Creature."""

    def __init__(self) -> None:
        super().__init__("Aquabub", "Water")

    def attack(self) -> str:
        return f"{self._name} uses Water Gun!"


class Torragon(Creature):
    """Evolved water-type Creature."""

    def __init__(self) -> None:
        super().__init__("Torragon", "Water")

    def attack(self) -> str:
        return f"{self._name} uses Hydro Pump!"
