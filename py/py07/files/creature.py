from abc import ABC, abstractmethod


class Creature(ABC):
    """Abstract base class for all Creature cards."""

    def __init__(self, name: str, creature_type: str) -> None:
        self._name = name
        self._type = creature_type

    @property
    def name(self) -> str:
        return self._name

    @property
    def creature_type(self) -> str:
        return self._type

    @abstractmethod
    def attack(self) -> str:
        pass

    def describe(self) -> str:
        return f"{self._name} is a {self._type} type Creature"
