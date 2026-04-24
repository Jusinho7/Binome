import sys
import typing


def read_file(filename: str) -> None:
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{filename}'")
    file: typing.IO[str] | None = None
    try:
        file = open(filename, "r")
    except OSError as e:
        print(f"Error opening file '{filename}': {e}")
        return
    print("---")
    content: str = file.read()
    print(content, end="")
    print("---")
    file.close()
    print(f"File '{filename}' closed.")


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>")
        return
    read_file(sys.argv[1])


if __name__ == "__main__":
    main()
