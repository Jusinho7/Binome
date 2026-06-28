from abc import ABC, abstractmethod

from ex0.creature import Creature
from ex0.creatures import Flameling, Pyrodon, Aquabub, Torragon


class CreatureFactory(ABC):
    """Abstract factory for creating Creature families."""

    @abstractmethod
    def create_base(self) -> Creature:
        pass

    @abstractmethod
    def create_evolved(self) -> Creature:
        pass


class FlameFactory(CreatureFactory):
    """Factory for fire-type Creatures."""

    def create_base(self) -> Creature:
        return Flameling()

    def create_evolved(self) -> Creature:
        return Pyrodon()


class AquaFactory(CreatureFactory):
    """Factory for water-type Creatures."""

    def create_base(self) -> Creature:
        return Aquabub()

    def create_evolved(self) -> Creature:
        return Torragon()
