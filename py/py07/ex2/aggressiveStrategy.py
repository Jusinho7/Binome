from ex0 import Creature
from ex1 import Transform
from .battleStrategy import BattleStrategy


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, target: Creature | None) -> bool:
        return isinstance(target, Transform)

    def act(self, target: Creature | None) -> None:
        if target is None or not self.is_valid(target):
            name = target.name if isinstance(target, Creature) else "None"
            raise ValueError(
                f"Invalid Creature '{name}'"
                f" for this aggressive strategy"
            )
        assert isinstance(target, Transform)
        print(target.transform())
        print(target.attack())
        print(target.revert())
