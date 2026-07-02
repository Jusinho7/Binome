from abc import ABC, abstractmethod
from ex0 import Creature


class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, target: Creature | None) -> bool: ...

    @abstractmethod
    def act(self, target: Creature | None) -> None: ...
