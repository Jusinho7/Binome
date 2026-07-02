from abc import ABC, abstractmethod


class Creature(ABC):
    @abstractmethod
    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species

    @abstractmethod
    def attack(self) -> str: ...

    def describe(self) -> str:
        return f"{self.name} is a {self.species} Creature"
