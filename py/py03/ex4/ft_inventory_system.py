import sys


def parse_inventory(args: list[str]) -> dict[str, int]:
    inventory: dict[str, int] = {}
    for arg in args:
        parts: list[str] = arg.split(":")
        if len(parts) != 2 or not parts[0] or not parts[1]:
            print(f"Error - invalid parameter '{arg}'")
            continue
        name: str = parts[0]
        quantity_str: str = parts[1]
        if name in inventory:
            print(f"Redundant item '{name}' - discarding")
            continue
        try:
            quantity: int = int(quantity_str)
            inventory[name] = quantity
        except ValueError as e:
            print(f"Quantity error for '{name}': {e}")
    return inventory


def main() -> None:
    print("=== Inventory System Analysis ===")

    inventory: dict[str, int] = parse_inventory(sys.argv[1:])

    if not inventory:
        print("Inventory is empty.")
        return

    print(f"Got inventory: {inventory}")

    items: list[str] = list(dict.keys(inventory))
    print(f"Item list: {items}")

    total: int = sum(dict.values(inventory))
    print(f"Total quantity of the {len(inventory)} items: {total}")

    for item, qty in inventory.items():
        pct: float = round(qty / total * 100, 1)
        print(f"Item {item} represents {pct}%")

    most: str = max(inventory, key=lambda k: (inventory[k], -items.index(k)))
    least: str = min(inventory, key=lambda k: (inventory[k], items.index(k)))
    print(f"Item most abundant: {most} with quantity {inventory[most]}")
    print(f"Item least abundant: {least} with quantity {inventory[least]}")

    inventory.update({"magic_item": 1})
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    main()
