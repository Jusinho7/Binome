#!/usr/bin/env python3
from typing import Sequence
from ex0 import Creature, Factory as CreatureFactory, Flame, Aqua
from ex1 import Healing, Transforming
from ex2 import normal, aggressive, defensive
from ex2 import strategy


def battle(
    opponents: Sequence[tuple[CreatureFactory, strategy]],
) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    creatures_and_strategies: list[tuple[Creature, strategy]] = []
    for factory, strat in opponents:
        creature = factory.create_base()
        creatures_and_strategies.append((creature, strat))

    for i, (attacker, attacker_strategy) in enumerate(
        creatures_and_strategies
    ):
        for j, (defender, defender_strategy) in enumerate(
            creatures_and_strategies
        ):
            if i >= j:
                continue

            print("* Battle *")
            print(attacker.describe())
            print("vs.")
            print(defender.describe())
            print("now fight!")

            if not attacker_strategy.is_valid(attacker):
                msg = (
                    f"Battle error, aborting tournament: "
                    f"Invalid Creature '{attacker.name}' "
                    f"for this strategy"
                )
                print(msg)
                return
            try:
                attacker_strategy.act(attacker)
            except ValueError as e:
                print(f"Battle error, aborting tournament: {e}")
                return

            if not defender_strategy.is_valid(defender):
                msg = (
                    f"Battle error, aborting tournament: "
                    f"Invalid Creature '{defender.name}' "
                    f"for this strategy"
                )
                print(msg)
                return
            try:
                defender_strategy.act(defender)
            except ValueError as e:
                print(f"Battle error, aborting tournament: {e}")
                return


def main() -> None:
    print("Tournament 0 (basic)")
    print("[ (Flameling+Normal), (Healing+Defensive) ]")
    battle([
        (Flame(), normal()),
        (Healing(), defensive()),
    ])

    print()

    print("Tournament 1 (error)")
    print("[ (Flameling+Aggressive), (Healing+Defensive) ]")
    battle([
        (Flame(), aggressive()),
        (Healing(), defensive()),
    ])

    print()

    print("Tournament 2 (multiple)")
    print(
        "[ (Aquabub+Normal), (Healing+Defensive), "
        "(Transform+Aggressive) ]"
    )
    battle([
        (Aqua(), normal()),
        (Healing(), defensive()),
        (Transforming(), aggressive()),
    ])


if __name__ == "__main__":
    main()
