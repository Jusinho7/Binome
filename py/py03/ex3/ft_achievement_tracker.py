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

    for name in players:
        print(f"Player {name}: {players[name]}")

    all_sets: list[set[str]] = []
    for name in players:
        all_sets += [players[name]]

    all_distinct: set[str] = set.union(*all_sets)
    print(f"\nAll distinct achievements: {all_distinct}")

    common: set[str] = set.intersection(*all_sets)
    print(f"Common achievements: {common}")

    for name in players:
        all_sets: list[set[str]] = []
        for n in players:
            if n != name:
                all_sets += [players[n]]
        others = set.union(*all_sets)
        only_player: set[str] = set.difference(players[name], others)
        print(f"Only {name} has: {only_player}")

    for name in players:
        missing = set.difference(all_distinct, players[name])
        print(f"{name} is missing: {missing}")


if __name__ == "__main__":
    main()
