from typing import List, Tuple, Set
from .generator import MazeGenerator


RESET  = "\033[0m"
RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
BLUE   = "\033[34m"
CYAN   = "\033[36m"
WHITE  = "\033[37m"
BG_BLUE   = "\033[44m"
BG_GREEN  = "\033[42m"
BG_RED    = "\033[41m"


def _path_cells(
    entry: Tuple[int, int],
    path: List[str],
) -> Set[Tuple[int, int]]:
    direction_delta = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
    cells = set()
    x, y = entry
    cells.add((x, y))
    for step in path:
        dx, dy = direction_delta[step]
        x += dx
        y += dy
        cells.add((x, y))
    return cells


def print_colored(
    maze: MazeGenerator,
    entry: Tuple[int, int],
    exit: Tuple[int, int],
    path: List[str],
    show_path: bool = True,
    wall_color: str = WHITE,
) -> None:
    path_cells = _path_cells(entry, path) if show_path else set()

    def wall(char: str) -> str:
        return wall_color + char + RESET

    def cell_char(x: int, y: int) -> str:
        if (x, y) == entry:
            return BG_GREEN + " E " + RESET
        if (x, y) == exit:
            return BG_RED + " S " + RESET
        if show_path and (x, y) in path_cells:
            return BG_BLUE + " . " + RESET
        return "   "

    print(wall("+" + "---+" * maze.width))

    for y in range(maze.height):
        row_top = wall("|")
        row_bot = wall("+")

        for x in range(maze.width):
            cell = maze.grid[y][x]
            row_top += cell_char(x, y)
            row_top += wall("|") if cell & MazeGenerator.EAST else " "
            row_bot += wall("---") if cell & MazeGenerator.SOUTH else "   "
            row_bot += wall("+")

        print(row_top)
        print(row_bot)