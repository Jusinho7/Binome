from abc import ABC, abstractmethod

from ex0.creature import Creature
from ex1.capabilities import HealCapability, TransformCapability


class BattleStrategy(ABC):
    """Abstract strategy for how a Creature fights in a tournament."""

    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        pass

    @abstractmethod
    def act(self, creature: Creature) -> None:
        pass


class NormalStrategy(BattleStrategy):
    """Strategy suitable for any Creature: simply attacks."""

    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> None:
        print(creature.attack())


class AggressiveStrategy(BattleStrategy):
    """Strategy for transform-capable Creatures: transform, attack, revert."""

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            raise ValueError(
                f"Invalid Creature '{creature.name}' for this aggressive strategy"
            )
        transform_creature = creature  # type: ignore[assignment]
        print(transform_creature.transform())  # type: ignore[union-attr]
        print(creature.attack())
        print(transform_creature.revert())  # type: ignore[union-attr]


class DefensiveStrategy(BattleStrategy):
    """Strategy for healing-capable Creatures: attack then heal."""

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            raise ValueError(
                f"Invalid Creature '{creature.name}' for this defensive strategy"
            )
        print(creature.attack())
        heal_creature = creature  # type: ignore[assignment]
        print(heal_creature.heal())  # type: ignore[union-attr]
