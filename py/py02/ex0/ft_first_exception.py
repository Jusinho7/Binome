def input_temperature(temp_str: str) -> int:
    return int(temp_str)


def test_temperature() -> None:
    print("=== Garden Temperature ===")
    print()

    tmp_list = ["25", "abc"]

    for temp_str in tmp_list:
        print()
        print(f"Input data is '{temp_str}'")
        try:
            result = input_temperature(temp_str)
            print(f"Temperature is now {result}°C")
        except ValueError as err:
            print(f"Caught input_temperature error: {err}")

    print()
    print("All tests completed - program didn't crash")


def main() -> None:
    test_temperature()


if __name__ == "__main__":
    main()
