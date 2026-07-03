"""ASCII terminal renderer for the maze."""

from frontend.colors import ANSI_RESET, ansi, ROLE_COLORS
from frontend.renderer_base import MazeLike, Renderer

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8
FULLY_CLOSED = NORTH | EAST | SOUTH | WEST

WALL_CHAR = "#"
EMPTY_CHAR = " "
ENTRY_CHAR = "S"
EXIT_CHAR = "X"
PATH_CHAR = "."
PATTERN_CHAR = "@"


class AsciiRenderer(Renderer):
    def draw(
        self,
        maze: MazeLike,
        show_path: bool,
        wall_color: str,
        pattern_color: str = "bold_white",
    ) -> None:
        try:
            grid, color_grid = self._build_grid(maze)
            found_pattern = self._mark_pattern_42(
                maze, grid, color_grid, pattern_color
            )
            if not found_pattern:
                print(
                    "[frontend] No fully-closed cell found: the '42' "
                    "pattern could not be highlighted (maze too small?)."
                )
            if show_path:
                self._mark_path(maze, grid, color_grid)
            self._mark_endpoints(maze, grid, color_grid)
            self._print_grid(grid, color_grid, wall_color)
        except (AttributeError, IndexError, ValueError) as exc:
            print(f"[frontend] Unable to render maze: {exc}")

    def _mark_pattern_42(
        self,
        maze: MazeLike,
        grid: list[list[str]],
        color_grid: list[list[str | None]],
        pattern_color: str,
    ) -> bool:
        found = False
        for y in range(maze.height):
            for x in range(maze.width):
                if maze.get_walls(x, y) == FULLY_CLOSED:
                    cy, cx = 2 * y + 1, 2 * x + 1
                    grid[cy][cx] = PATTERN_CHAR
                    color_grid[cy][cx] = pattern_color
                    found = True
        return found

    def close(self) -> None:
        return None

    def _build_grid(
        self, maze: MazeLike
    ) -> tuple[list[list[str]], list[list[str | None]]]:
        rows = 2 * maze.height + 1
        cols = 2 * maze.width + 1
        grid = [[WALL_CHAR for _ in range(cols)] for _ in range(rows)]
        color_grid: list[list[str | None]] = [
            [None] * cols for _ in range(rows)
        ]

        for y in range(maze.height):
            for x in range(maze.width):
                walls = maze.get_walls(x, y)
                cy, cx = 2 * y + 1, 2 * x + 1
                grid[cy][cx] = EMPTY_CHAR
                grid[cy - 1][cx] = WALL_CHAR if walls & NORTH else EMPTY_CHAR
                grid[cy + 1][cx] = WALL_CHAR if walls & SOUTH else EMPTY_CHAR
                grid[cy][cx - 1] = WALL_CHAR if walls & WEST else EMPTY_CHAR
                grid[cy][cx + 1] = WALL_CHAR if walls & EAST else EMPTY_CHAR
        return grid, color_grid

    def _mark_path(
        self,
        maze: MazeLike,
        grid: list[list[str]],
        color_grid: list[list[str | None]],
    ) -> None:
        direction_delta = {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "W": (-1, 0),
        }
        x, y = maze.entry
        for step in maze.get_solution_path():
            dx, dy = direction_delta.get(step, (0, 0))
            x, y = x + dx, y + dy
            cy, cx = 2 * y + 1, 2 * x + 1
            if grid[cy][cx] == EMPTY_CHAR:
                grid[cy][cx] = PATH_CHAR
                color_grid[cy][cx] = ROLE_COLORS["path"]

    def _mark_endpoints(
        self,
        maze: MazeLike,
        grid: list[list[str]],
        color_grid: list[list[str | None]],
    ) -> None:
        ex, ey = maze.entry
        xx, xy = maze.exit
        grid[2 * ey + 1][2 * ex + 1] = ENTRY_CHAR
        color_grid[2 * ey + 1][2 * ex + 1] = ROLE_COLORS["entry"]
        grid[2 * xy + 1][2 * xx + 1] = EXIT_CHAR
        color_grid[2 * xy + 1][2 * xx + 1] = ROLE_COLORS["exit"]

    def _print_grid(
        self,
        grid: list[list[str]],
        color_grid: list[list[str | None]],
        wall_color: str,
    ) -> None:
        for row_idx, row in enumerate(grid):
            line_parts = []
            for col_idx, char in enumerate(row):
                color = color_grid[row_idx][col_idx]
                if char == WALL_CHAR:
                    color = wall_color
                if color:
                    line_parts.append(f"{ansi(color)}{char}{ANSI_RESET}")
                else:
                    line_parts.append(char)
            print("".join(line_parts))
