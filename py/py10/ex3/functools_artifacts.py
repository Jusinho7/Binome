from functools import reduce, partial, lru_cache, singledispatch
from operator import add, mul
from collections.abc import Callable
from random import randint, choice
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0
    op: dict[str, Callable[[int, int], int]] = {
        "add": add,
        "multiply": mul,
        "max": max,
        "min": min
    }
    if operation not in op:
        print(f"[ERROR]: unknown operation '{operation}'")
        return 0
    return reduce(op[operation], spells, 0)


def base_enchantment(power: int, element: str, target: str) -> str:
    return f"{target} is enchanted with {element} (power {power})"


def partial_enchanter(
        base_enchantment: Callable[[int, str, str], str]
        ) -> dict[str, partial[str]]:
    fire_enchant: partial[str] = partial(
        base_enchantment,
        power=50,
        element="fire")
    ice_enchant: partial[str] = partial(
        base_enchantment,
        power=50,
        element="ice")
    lightning_enchant: partial[str] = partial(
        base_enchantment,
        power=50,
        element="lightning"
    )
    return {
        "fire": fire_enchant,
        "ice": ice_enchant,
        "lightning": lightning_enchant
    }


@lru_cache(maxsize=128)
def memoized_fibonacci(n: int) -> int:
    if n < 2:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    @singledispatch
    def cast(spell: Any) -> str:
        return "Unknown spell type"

    @cast.register
    def _(spell: int) -> str:
        return f"Damage spell: {spell} damage"

    @cast.register
    def _(spell: str) -> str:
        return f"Enchantment: {spell}"

    @cast.register
    def _(spell: list[Any]) -> str:
        return f"Multi-cast: {len(spell)} spells"

    return cast


def main() -> None:
    spell_powers = [43, 32, 30, 27, 25, 29]
    operations = ['add', 'multiply', 'max', 'min']
    assets = ['Dragon', 'Goblin', 'Wizard', 'Knight']

    print("\nTesting spell reducer...")
    for op in operations:
        result = spell_reducer(spell_powers, op)
        print(f"{op}: {result}")

    print("\nTesting partial_enchanter...")
    enchants = partial_enchanter(base_enchantment)
    print(enchants["fire"](target="Sword"))
    print(enchants["ice"](target="Sword"))
    print(enchants["lightning"](target="Sword"))

    print("\nTesting memoized fibonacci...")
    y: int = randint(1, 4)
    for i in range(y):
        x: int = randint(0, 20)
        print(f"Fib({x}): {memoized_fibonacci(x)}")
        print(f"Cache info: {memoized_fibonacci.cache_info()}")

    print("\nTesting spell dispatcher...")
    spells: list[int] = []
    spell_count: int = randint(1, 5)
    number: int = randint(0, 100)
    item = choice(assets)
    for _ in range(spell_count):
        r: int = randint(0, 10)
        spells.append(r)
    launch = spell_dispatcher()
    print(launch(number))
    print(launch(item))
    print(launch(spells))
    print(launch(0.1))


if __name__ == "__main__":
    main()
