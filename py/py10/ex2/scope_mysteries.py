from collections.abc import Callable
from random import randrange, choice
from typing import Any


def mage_counter() -> Callable[[], int]:
    count: int = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count

    return counter


def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    power: int = initial_power

    def accumulator(add: int) -> int:
        nonlocal power
        power += add
        return power

    return accumulator


def enchantment_factory(enchantment_type: str) -> Callable[[str], str]:

    def factory(item: str) -> str:
        return f"{enchantment_type} {item}"

    return factory


def memory_vault() -> dict[str, Callable[..., Any]]:
    memory: dict[str, Any] = {}

    def store(key: str, value: Any) -> None:
        memory[key] = value

    def recall(key: str) -> Any:
        return memory.get(key, "Memory not found")

    return {"store": store, "recall": recall}


def main() -> None:
    enchantment_types = ["Flowing", "Flaming", "Earthen"]
    items_to_enchant = ["Armor", "Wand", "Ring", "Amulet"]
    enchantment: str = choice(enchantment_types)
    item: str = choice(items_to_enchant)

    print("Testing mage counter...")
    times1: int = randrange(2, 5)
    mage1 = mage_counter()
    for i in range(times1):
        print(f"Counter_a call {i}: {mage1()}")

    print("\nTesting spell accumulator...")
    x: int = 100
    times2: int = randrange(2, 5)
    for _ in range(times2):
        y: int = randrange(10, 100, 10)
        base1 = spell_accumulator(x)
        print(f"Base {x}, add {y}: {base1(y)}")

    print("\nTesting enchantment factory...")
    fact = enchantment_factory(enchantment)
    print(fact(item))

    print("\nTesting memory vault...")
    val = memory_vault()
    val["store"]("secret", 42)
    print("Store 'secret' = 42")
    print(f"Recall 'secret': {val['recall']('secret')}")
    print(f"Recall 'unknown': {val['recall']('unknown')}")


if __name__ == "__main__":
    main()
