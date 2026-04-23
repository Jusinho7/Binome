def garden_operations(operation_number: int) -> None:
    if operation_number == 0:
        int("abc")
    elif operation_number == 1:
        10 / 0
    elif operation_number == 2:
        with open("/non/existent/file"):
            pass
    elif operation_number == 3:
        x: str = "string"
        y: int = 42
        x + y


def test_error_types() -> None:
    print("=== Garden Error Types Demo ===")

    for operation_num in range(5):
        print(f"Testing operation {operation_num}...")
        try:
            garden_operations(operation_num)
            print("Operation completed successfully")
        except (
            ValueError,
            ZeroDivisionError,
            FileNotFoundError,
            TypeError,
        ) as err:
            print(f"Caught {type(err).__name__}: {err}")

    print()
    print("All error types tested successfully!")


def main() -> None:
    test_error_types()


if __name__ == "__main__":
    main()
