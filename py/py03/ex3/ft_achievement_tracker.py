import random


ALL_ACHIEVEMENTS: list[str] = [
    "First Steps", "Speed Runner", "Boss Slayer", "Treasure Hunter",
    "Survivor", "Strategist", "Master Explorer", "Crafting Genius",
    "World Savior", "Unstoppable", "Untouchable", "Collector Supreme",
    "Sharp Mind", "Hidden Path Finder", "Dragon Tamer", "Pacifist",
    "Night Owl", "Completionist", "Lucky Star", "Iron Will",
]


def gen_player_achievements() -> set[str]:
    count: int = random.randint(4, 10)
    return set(random.sample(ALL_ACHIEVEMENTS, count))


def main() -> None:
    print("=== Achievement Tracker System ===")

    players: dict[str, set[str]] = {
        "Alice": gen_player_achievements(),
        "Bob": gen_player_achievements(),
        "Charlie": gen_player_achievements(),
        "Dylan": gen_player_achievements(),
    }

    for name, achievements in players.items():
        print(f"Player {name}: {achievements}")

    all_sets: list[set[str]] = list(players.values())

    all_distinct: set[str] = set.union(*all_sets)
    print(f"\nAll distinct achievements: {all_distinct}")

    common: set[str] = set.intersection(*all_sets)
    print(f"Common achievements: {common}")

    for name, achievements in players.items():
        others: set[str] = set.union(
            *[a for n, a in players.items() if n != name]
        )
        only_player: set[str] = set.difference(achievements, others)
        missing: set[str] = set.difference(all_distinct, achievements)
        print(f"Only {name} has: {only_player}")

    for name, achievements in players.items():
        missing = set.difference(all_distinct, achievements)
        print(f"{name} is missing: {missing}")


if __name__ == "__main__":
    main()
