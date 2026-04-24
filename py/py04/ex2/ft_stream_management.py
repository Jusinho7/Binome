import sys
import typing


def read_file(filename: str) -> str | None:
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{filename}'")
    file: typing.IO[str] | None = None
    try:
        file = open(filename, "r")
    except OSError as e:
        sys.stderr.write(f"[STDERR] Error opening file '{filename}': {e}\n")
        sys.stderr.flush()
        return None
    print("---")
    content: str = file.read()
    sys.stdout.write(content)
    sys.stdout.flush()
    print("---")
    file.close()
    print(f"File '{filename}' closed.")
    return content


def transform_content(content: str) -> str:
    lines: list[str] = content.splitlines()
    new_lines: list[str] = [line + "#" for line in lines]
    return "\n".join(new_lines) + "\n"


def save_file(filename: str, content: str) -> bool:
    print(f"Saving data to '{filename}'")
    file: typing.IO[str] | None = None
    try:
        file = open(filename, "w")
    except OSError as e:
        sys.stderr.write(f"[STDERR] Error opening file '{filename}': {e}\n")
        sys.stderr.flush()
        return False
    file.write(content)
    file.close()
    print(f"Data saved in file '{filename}'.")
    return True


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
    sys.stdout.write(new_content)
    sys.stdout.flush()
    print("---")
    sys.stdout.write("Enter new file name (or empty): ")
    sys.stdout.flush()
    save_name: str = sys.stdin.readline().rstrip("\n")
    if not save_name:
        print("Not saving data.")
        return
    saved: bool = save_file(save_name, new_content)
    if not saved:
        print("Data not saved.")


if __name__ == "__main__":
    main()
