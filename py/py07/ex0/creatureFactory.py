from abc import ABC, abstractmethod
from .creature import Creature


class CreatureFactory(ABC):
    @abstractmethod
    def create_base(self) -> Creature: ...

    @abstractmethod
    def create_evolved(self) -> Creature:  ...
