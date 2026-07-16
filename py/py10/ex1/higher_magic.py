from collections.abc import Callable


def fireball(target: str, power: int) -> str:
    return f"Fireball restores {target} or {power} HP"


def heal(target: str, power: int) -> str:
    return f"Heal restores {target} for {power} HP"


def spell_combiner(
        spell1: Callable[[str, int], str],
        spell2: Callable[[str, int], str]
    ) -> Callable[[] ,tuple[str, int]]:
    def combined(target: str, power: int) -> tuple:
        result1 = spell1(target, power)
        result2 = spell2(target, power)
        return (result1, result2)
    return combined


def main() -> None:
    combined = spell_combiner(fireball, heal)
    result = combined("Dinos", 20)
    print(result)


if __name__ == "__main__":
    main()
