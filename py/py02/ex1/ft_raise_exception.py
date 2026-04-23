def input_temperature(temp_str: str) -> int:
    temperature = int(temp_str)
    if temperature > 40:
        raise ValueError(f"{temperature}°C is too hot for plants (max 40°C)")
    if temperature < 0:
        raise ValueError(f"{temperature}°C is too cold for plants (min 0°C)")
    return temperature


def test_temperature() -> None:
    print("=== Garden Temperature Checker ===")

    tmp_list = ["25", "abc", "100", "-50"]

    for temp_str in tmp_list:
        print()
        print(f"Input data is '{temp_str}'")
        try:
            result = input_temperature(temp_str)
            print(f"Temperature is now {result}°C")
        except ValueError as err:
            print(f"Caught input_temperature error: {err}")

    print()
    print("All tests completed - program didn't crash!")


def main() -> None:
    test_temperature()


if __name__ == "__main__":
    main()
