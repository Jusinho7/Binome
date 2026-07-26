"""Writes the generated maze to disk in the subject's hexadecimal format."""

from mazegen import MazeGenerator


def write_maze_file(path: str, generator: MazeGenerator) -> None:
    walls = generator.get_walls()
    path_str = generator.shortest_path()

    lines: list[str] = []
    for row in walls:
        lines.append("".join(f"{cell:X}" for cell in row))
    lines.append("")
    lines.append(f"{generator.entry[0]},{generator.entry[1]}")
    lines.append(f"{generator.exit[0]},{generator.exit[1]}")
    lines.append(path_str)

    with open(path, "w", encoding="utf-8") as handle:
        for line in lines:
            handle.write(line + "\n")
