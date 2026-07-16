from collections.abc import Callable
from random import choice, randint


def fireball(target: str, power: int) -> str:
    return f"Fireball restores {target} or {power} HP"


def heal(target: str, power: int) -> str:
    return f"Heal restores {target} for {power} HP"


def check_power(power: int) -> bool:
    return power >= 10


def spell_combiner(
    spell1: Callable[[str, int], str],
    spell2: Callable[[str, int], str],
) -> Callable[[str, int], tuple[str, str]]:
    def combined(target: str, power: int) -> tuple[str, str]:
        if not callable(spell1) or not callable(spell2):
            return ("[ERROR]: spell1 or spell2 is not callable", "")
        result1: str = spell1(target, power)
        result2: str = spell2(target, power)
        return (result1, result2)
    return combined


def power_amplifier(
    base_spell: Callable[[str, int], str],
    multiplier: int,
) -> Callable[[str, int], str]:
    def amplified(target: str, power: int) -> str:
        if not callable(base_spell):
            return "[ERROR]: base_spell is not callable"
        if multiplier < 0:
            return "[ERROR]: multiplier cannot be negative"
        elif multiplier == 0:
            return "[WARNING]: multiplier cannot be null"
        else:
            new_power = power * multiplier
            return base_spell(target, new_power)
    return amplified


def conditional_caster(
    condition: Callable[[int], bool],
    spell: Callable[[str, int], str],
) -> Callable[[str, int], str]:
    def cast(target: str, power: int) -> str:
        if not callable(condition) or not callable(spell):
            return "[ERROR]: spell is not callable"
        if condition(power):
            return spell(target, power)
        else:
            return "Spell fizzled"
    return cast


def spell_sequence(
    spells: list[Callable[[str, int], str]],
) -> Callable[[str, int], list[str]]:
    def sequences(target: str, power: int) -> list[str]:
        res: list[str] = []
        for spell in spells:
            if not callable(spell):
                res.append("[ERROR]: spell is not callable")
            else:
                res.append(spell(target, power))
        return res
    return sequences


def main() -> None:
    test_values = [18, 11, 9]
    test_targets = ['Dragon', 'Goblin', 'Wizard', 'Knight']
    target = choice(test_targets)
    value = choice(test_values)

    print("Testing spell combiner...")
    combined = spell_combiner(fireball, heal)
    result_combined = combined(target, value)
    if not result_combined[1]:
        print(f"Combined spell result: {result_combined[0]}")
    else:
        print(f"Combined spell result: {', '.join(result_combined)}")

    print("\nTesting power amplifier...")
    x = randint(-5, 5)
    mega_fireball = power_amplifier(fireball, x)
    print(
        f"Original power: {value}, Multiplier: x{x}, "
        f"Amplified power: {value * x}"
    )
    result_amplified = mega_fireball(target, value)
    print(f"Result: {result_amplified}")

    print("\nTesting condition caster...")
    condition = conditional_caster(check_power, fireball)
    result_condition = condition(target, value)
    print(result_condition)

    print("\nTesting spell sequence...")
    sequences = spell_sequence([fireball, heal])
    result_sequence = sequences(target, value)
    print(' | '.join(result_sequence))


if __name__ == "__main__":
    main()
