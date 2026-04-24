import sys


def main() -> None:
    args: list[str] = sys.argv
    print("=== Command Quest ===")
    print(f"Program name: {args[0]}")

    if len(args) == 1:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {len(args) - 1}")
        for i, arg in enumerate(args[1:], start=1):
            print(f"Argument {i}: {arg}")

    print(f"Total arguments: {len(args)}")


if __name__ == "__main__":
    main()
