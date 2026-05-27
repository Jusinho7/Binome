# mazegen/writer.py
from typing import List, Tuple
from .generator import MazeGenerator


def write_output(
    maze: MazeGenerator,
    filepath: str,
    entry: Tuple[int, int],
    exit: Tuple[int, int],
    path: List[str],
) -> None:
    with open(filepath, "w") as f:
        for line in maze.to_hex_lines():
            f.write(line + "\n")

        f.write("\n")
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit[0]},{exit[1]}\n")
        f.write("".join(path) + "\n")