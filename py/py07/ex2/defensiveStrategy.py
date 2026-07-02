from typing import cast, Protocol
from ex0 import Creature
from ex1 import Heal
from .battleStrategy import BattleStrategy


class HealingCreature(Protocol):
    def attack(self) -> str: ...
    def heal(self, target: object | None = None) -> str: ...


class DefensiveStrategy(BattleStrategy):
    def is_valid(self, target: Creature | None) -> bool:
        return isinstance(target, Heal)

    def act(self, target: Creature | None) -> None:
        if target is None or not self.is_valid(target):
            name = target.name if isinstance(target, Creature) else "None"
            raise ValueError(
                f"Invalid Creature '{name}'"
                f" for this defensive strategy"
            )
        healer = cast(HealingCreature, target)
        print(healer.attack())
        print(healer.heal())
