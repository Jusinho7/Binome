# mazegen/generator.py
import random
from typing import List, Tuple, Optional


class MazeGenerator:
    NORTH = 1
    EAST  = 2
    SOUTH = 4
    WEST  = 8

    OPPOSITE = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
    DELTA    = {NORTH: (0, -1), SOUTH: (0, 1), EAST: (1, 0), WEST: (-1, 0)}

    def __init__(
        self,
        width: int,
        height: int,
        seed: Optional[int] = None,
        perfect: bool = True,
    ) -> None:
        self.width = width
        self.height = height
        self.perfect = perfect
        self.rng = random.Random(seed)

        self.grid: List[List[int]] = [
            [0xF] * width for _ in range(height)
        ]
        self._visited: List[List[bool]] = [
            [False] * width for _ in range(height)
        ]

        self._dfs(0, 0)

    def _in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def _open_wall(self, x: int, y: int, direction: int) -> None:
        dx, dy = self.DELTA[direction]
        nx, ny = x + dx, y + dy

        self.grid[y][x]   &= ~direction
        self.grid[ny][nx] &= ~self.OPPOSITE[direction]

    def _dfs(self, x: int, y: int) -> None:
        self._visited[y][x] = True

        directions = [self.NORTH, self.EAST, self.SOUTH, self.WEST]
        self.rng.shuffle(directions)

        for direction in directions:
            dx, dy = self.DELTA[direction]
            nx, ny = x + dx, y + dy

            if self._in_bounds(nx, ny) and not self._visited[ny][nx]:
                self._open_wall(x, y, direction)
                self._dfs(nx, ny)

    def get_cell(self, x: int, y: int) -> int:
        return self.grid[y][x]

    def to_hex_lines(self) -> List[str]:
        return [
            "".join(f"{cell:X}" for cell in row)
            for row in self.grid
        ]

    def print_ascii(self) -> None:
        print("+" + "---+" * self.width)
        for y in range(self.height):
            row_top = "|"
            row_bot = "+"
            for x in range(self.width):
                cell = self.grid[y][x]
                row_top += "   " + ("|" if cell & self.EAST else " ")
                row_bot += ("---" if cell & self.SOUTH else "   ") + "+"
            print(row_top)
            print(row_bot)
