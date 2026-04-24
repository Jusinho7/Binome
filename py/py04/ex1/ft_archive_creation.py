import sys
import typing


def read_file(filename: str) -> str | None:
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{filename}'")
    file: typing.IO[str] | None = None
    try:
        file = open(filename, "r")
    except OSError as e:
        print(f"Error opening file '{filename}': {e}")
        return None
    print("---")
    content: str = file.read()
    print(content, end="")
    print("---")
    file.close()
    print(f"File '{filename}' closed.")
    return content


def transform_content(content: str) -> str:
    lines: list[str] = content.splitlines()
    new_lines: list[str] = [line + "#" for line in lines]
    return "\n".join(new_lines) + "\n"


def save_file(filename: str, content: str) -> None:
    print(f"Saving data to '{filename}'")
    file: typing.IO[str] | None = None
    try:
        file = open(filename, "w")
    except OSError as e:
        print(f"Error opening file '{filename}': {e}")
        return
    file.write(content)
    file.close()
    print(f"Data saved in file '{filename}'.")


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>")
        return
    content: str | None = read_file(sys.argv[1])
    if content is None:
        return
    new_content: str = transform_content(content)
    print("\nTransform data:")
    print("---")
    print(new_content, end="")
    print("---")
    save_name: str = input("Enter new file name (or empty): ")
    if not save_name:
        print("Not saving data.")
        return
    save_file(save_name, new_content)


if __name__ == "__main__":
    main()
