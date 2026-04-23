class GardenError(Exception):
    def __init__(self, message: str = "Unknown garden error") -> None:
        self.message = message
        super().__init__(self.message)


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)


class WaterError(GardenError):
    def __init__(self, message: str = "Unknown water error") -> None:
        super().__init__(message)


def test_plant_error() -> None:
    try:
        raise PlantError("The tomato plant is wilting!")
    except PlantError as err:
        print(f"Caught PlantError: {err}")


def test_water_error() -> None:
    try:
        raise WaterError("Not enough water in the tank!")
    except WaterError as err:
        print(f"Caught WaterError: {err}")


def test_catch_all_garden_errors() -> None:
    errors_to_test = [
        PlantError("The tomato plant is wilting!"),
        WaterError("Not enough water in the tank!"),
    ]

    for error in errors_to_test:
        try:
            raise error
        except GardenError as err:
            print(f"Caught GardenError: {err}")


def main() -> None:
    print("=== Custom Garden Errors Demo ===")
    print()

    print("Testing PlantError...")
    test_plant_error()
    print()

    print("Testing WaterError...")
    test_water_error()
    print()

    print("Testing catching all garden errors...")
    test_catch_all_garden_errors()
    print()

    print("All custom error types work correctly!")


if __name__ == "__main__":
    main()
