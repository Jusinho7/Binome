from ex0 import Creature
from .battleStrategy import BattleStrategy


class NormalStrategy(BattleStrategy):
    def is_valid(self, target: Creature | None) -> bool:
        return isinstance(target, Creature)

    def act(self, target: Creature | None) -> None:
        if target is None or not self.is_valid(target):
            name = target.name if isinstance(target, Creature) else "None"
            raise ValueError(
                f"Invalid Creature '{name}' for this normal strategy"
            )
        print(target.attack())
