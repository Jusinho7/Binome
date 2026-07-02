#!/usr/bin/env python3
from typing import Protocol, cast
from ex1 import Healing, Transforming


class HealingCreature(Protocol):
    def describe(self) -> str: ...
    def attack(self) -> str: ...
    def heal(self, target: object | None = None) -> str: ...


class TransformCreature(Protocol):
    def describe(self) -> str: ...
    def attack(self) -> str: ...
    def transform(self) -> str: ...
    def revert(self) -> str: ...


def test_healing(factory: Healing) -> None:
    print("Testing Creature with healing capability\n base:")
    base = cast(HealingCreature, factory.create_base())
    print(base.describe())
    print(base.attack())
    print(base.heal())
    print(" evolved:")
    evolved = cast(HealingCreature, factory.create_evolved())
    print(evolved.describe())
    print(evolved.attack())
    print(evolved.heal())


def test_transform(factory: Transforming) -> None:
    print("\nTesting Creature with transform capability \n base:")
    base = cast(TransformCreature, factory.create_base())
    print(base.describe())
    print(base.attack())
    print(base.transform())
    print(base.attack())
    print(base.revert())
    print(" evolved:")
    evolved = cast(TransformCreature, factory.create_evolved())
    print(evolved.describe())
    print(evolved.attack())
    print(evolved.transform())
    print(evolved.attack())
    print(evolved.revert())


if __name__ == "__main__":
    test_healing(Healing())
    test_transform(Transforming())
