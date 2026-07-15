from typing import Any


def artifact_sorter(artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not artifacts:
        return []
    try:
        return sorted(artifacts, key=lambda x: x['power'], reverse=True)
    except KeyError:
        return [{"error": "missing key"}]


def power_filter(
        mages: list[dict[str, Any]], min_power: int) -> list[dict[str, Any]]:
    if not mages:
        return []
    try:
        return list(filter(lambda x: x['power'] >= min_power, mages))
    except KeyError:
        return [{"error": "missing key"}]


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda x: (f"* {x} *"), spells))


def mage_stats(mages: list[dict[str, Any]]) -> dict[str, Any]:
    if not mages:
        return {}
    try:
        min_power = min(mages, key=lambda x: x['power'])
        max_power = max(mages, key=lambda x: x['power'])
        avg_power = round(sum(x['power'] for x in mages) / len(mages), 2)
        return {
            "min_power": min_power['power'],
            "max_power": max_power['power'],
            "avg_power": avg_power
        }
    except KeyError:
        return {"error": "missing key"}


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

    print("\nTesting artifact sorter...")
    if not art:
        print("[WARNING]: No artifacts to display.")
    elif art and "error" in art[0]:
        print("[Error]: key is not found")
    else:
        print(' -> '.join(f"{a['name']}:({a['power']})" for a in art))

    print("\nTesting power filter...")
    if not power:
        print("[WARNING]: No mages to display.")
    elif power and "error" in power[0]:
        print("[Error]: key is not found")
    else:
        for m in power:
            print(f" - {m['name']}: {m['power']}")

    print("\nTesting spell transformer...")
    print(' '.join(spell) if spell else "List is empty.")

    print("\nTesting mages stats...")
    if not mage:
        print("[WARNING]: No mages to display.")
    elif "error" in mage:
        print("[Error]: key is not found")
    else:
        for key, item in mage.items():
            print(f"{key} = {item}")


if __name__ == "__main__":
    main()
