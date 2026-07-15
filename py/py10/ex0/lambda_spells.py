from typing import Any


def artifact_sorter(artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(artifacts, key=lambda x: x['power'], reverse=True)


def power_filter(
        mages: list[dict[str, Any]], min_power: int) -> list[dict[str, Any]]:
    return list(filter(lambda x: x['power'] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda x: (f"* {x} *"), spells))


def mage_stats(mages: list[dict[str, Any]]) -> dict[str, Any]:
    min_power = min(mages, key=lambda x: x['power'])
    max_power = max(mages, key=lambda x: x['power'])
    avg_power = round(sum(x['power'] for x in mages) / len(mages), 2)
    return {
        "min_power": min_power['power'],
        "max_power": max_power['power'],
        "avg_power": avg_power
    }


def main() -> None:
    artifacts = [
        {'name': 'Light Prism', 'power': 86, 'type': 'relic'},
        {'name': 'Lightning Rod', 'power': 114, 'type': 'weapon'},
        {'name': 'Earth Shield', 'power': 67, 'type': 'focus'},
        {'name': 'Light Prism', 'power': 83, 'type': 'weapon'}
    ]
    mages = [
        {'name': 'Storm', 'power': 67, 'element': 'ice'},
        {'name': 'Ash', 'power': 89, 'element': 'shadow'},
        {'name': 'Rowan', 'power': 73, 'element': 'fire'},
        {'name': 'Alex', 'power': 83, 'element': 'ice'},
        {'name': 'River', 'power': 57, 'element': 'light'}
    ]
    spells = ['blizzard', 'darkness', 'meteor', 'lightning']

    art = artifact_sorter(artifacts)
    power = power_filter(mages, 57)
    spell = spell_transformer(spells)
    mage = mage_stats(mages)

    print(
        "\nTesting artifact sorter...\n"
        f"{art[0]['name']} ({art[0]['power']} power) comes before "
        f"{art[1]['name']} ({art[1]['power']} power)"
    )

    print("\nTesting power filter...")
    for m in power:
        print(f" {m['name']} ({m['power']} power)")

    print("\nTesting spell transformer...")
    print(' '.join(spell))

    print("\nTesting mages stats...")
    for key, item in mage.items():
        print(f"{key} = {item}")


if __name__ == "__main__":
    main()
