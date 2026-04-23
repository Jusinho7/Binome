class GardenError(Exception):
    def __init__(self, message: str = "Unknown garden error") -> None:
        self.message = message
        super().__init__(self.message)


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)


def water_plant(plant_name: str) -> None:
    if plant_name != plant_name.capitalize():
        raise PlantError(f"Invalid plant name to water: '{plant_name}'")
    print(f"Watering {plant_name}: [OK]")


def test_watering_system(plants: list) -> None:
    try:
        print("Opening watering system")
        for plant in plants:
            water_plant(plant)
    except PlantError as err:
        print(f"Caught PlantError: {err}")
        print(".. ending tests and returning to main")
        return
    finally:
        print("Closing watering system")


def main() -> None:
    print("=== Garden Watering System ===")
    print()

    print("Testing valid plants...")
    test_watering_system(["Tomato", "Lettuce", "Carrots"])
    print()

    print("Testing invalid plants...")
    test_watering_system(["Tomato", "lettuce"])
    print()

    print("Cleanup always happens, even with errors!")


if __name__ == "__main__":
    main()
