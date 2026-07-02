#!/usr/bin/env python3
from ex0 import Factory, Flame, Aqua


def test_factory(factory: Factory) -> None:
    base = factory.create_base()
    evolved = factory.create_evolved()
    print(base.describe())
    print(base.attack())
    print(evolved.describe())
    print(evolved.attack())


def test_battle(factory1: Factory, factory2: Factory) -> None:
    c1 = factory1.create_base()
    c2 = factory2.create_base()
    print(f"{c1.describe()} vs {c2.describe()} fight!")
    print(c1.attack())
    print(c2.attack())


def main() -> None:
    print("Testing factory")
    flame = Flame()
    test_factory(flame)
    print("\nTesting factory")
    aqua = Aqua()
    test_factory(aqua)
    print("\nTesting battle")
    test_battle(flame, aqua)


if __name__ == "__main__":
    main()
