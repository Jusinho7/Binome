def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
    if unit == "packets":
        print(f"{seed_type.capitalize()} seeds: {quantity} packets availaible")
    elif unit == "grams":
        print(f"{seed_type.capitalize()} seeds: {quantity} grams")
    elif unit == "area":
        print(f"{seed_type.capitalize()} seeds: covers {quantity} meters")
