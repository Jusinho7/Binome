from collections.abc import Callable
from functools import wraps
from time import time
from random import choice, random
from typing import Any


def spell_timer(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Casting {func.__name__}...")
        start = time()
        result = func(*args, **kwargs)
        end = time()
        duration = end - start
        print(f"Spell completed in {duration:.3f} seconds")
        return result
    return wrapper


@spell_timer
def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target} for {power} damage"


def power_validator(min_power: int) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            power: Any
            if "power" in kwargs:
                power = kwargs["power"]
            elif args:
                power = args[0]
            else:
                return "Insufficient power for this spell"

            if power >= min_power:
                return func(*args, **kwargs)
            else:
                return "Insufficient power for this spell"
        return wrapper
    return decorator


@power_validator(min_power=10)
def cast_lightning(power: int, target: str) -> str:
    return f"Lightning strikes {target} with {power} power"


def retry_spell(max_attempts: int) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempts in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    print(
                        f"Spell failed, retrying... "
                        f"(attempt {attempts}/{max_attempts})"
                    )
            return f"Spell casting failed after {max_attempts} attempts"
        return wrapper
    return decorator


@retry_spell(max_attempts=3)
def unstable_spell(target: str) -> str:
    if random() < 0.7:
        raise ValueError("The spell fizzled unexpectedly!")
    return f"Successfully cast on {target}"


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        if len(name) < 3:
            return False
        return name.replace(" ", "").isalpha()

    def cast_spell(self, spell_name: str, power: int) -> str:
        if power >= 10:
            return f"Successfully cast {spell_name} with {power} power"
        else:
            return "Insufficient power for this spell"


def main() -> None:
    test_powers: list[int] = [20, 23, 5, 23]
    spell_names: list[str] = ['lightning', 'earthquake', 'freeze', 'fireball']
    mage_names: list[str] = ['Sage', 'Ember', 'Riley', 'Kai', 'Casey', 'Storm']
    invalid_names: list[str] = ['Jo', 'A', 'Alex123', 'Test@Name']

    power: int = choice(test_powers)
    spell: str = choice(spell_names)
    name: str = choice(mage_names)
    invalid: str = choice(invalid_names)

    print("Testing spell timer...")
    run: str = fireball(name, power)
    print(f"Result: {run}")

    print("\nTesting power validator...")
    run = cast_lightning(power, name)
    print(f"Result: {run}")

    print("\nTesting retrying spell...")
    run = unstable_spell(name)
    print(f"Result: {run}")

    print("\nTesting MageGuild...")
    test1: bool = MageGuild.validate_mage_name(name)
    test2: bool = MageGuild.validate_mage_name(invalid)
    print(test1)
    print(test2)

    guild = MageGuild()
    result_success: str = guild.cast_spell(spell, power)
    print(result_success)


if __name__ == "__main__":
    main()
