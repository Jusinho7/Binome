"""
Mock maze generator so the frontend can be built and tested standalone.
This is NOT the real maze generation algorithm. It produces a random,
not-necessarily-valid, grid just to exercise the rendering and interaction
code before the backend's real MazeGenerator is ready.
Replace usages of MockMaze with the real backend class once integrated
(as long as it satisfies the same MazeLike interface, no other change
is needed in the frontend).
"""
import random

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8


class MockMaze:
    def __init__(
        self,
        width: int = 10,
        height: int = 8,
        entry: tuple[int, int] = (0, 0),
        exit: tuple[int, int] = (9, 7),
        seed: int | None = None
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self._rng = random.Random(seed)
        self._walls: dict[tuple[int, int], int] = {}
        self.regenerate(seed)

    def regenerate(self, seed: int | None = None) -> None:
        if seed is not None:
            self._rng = random.Random(seed)
        self._walls = {
            (x, y): self._rng.randint(0, 15)
            for x in range(self.width)
            for y in range(self.height)
        }

    def get_walls(self, x: int, y: int) -> int:
        return self._walls[(x, y)]

    def get_solution(self) -> list[str]:
        path: list[str] = []
        x, y = self.entry
        tx, ty = self.exit
        while x != tx:
            path.append("E" if tx > x else "W")
            x += 1 if tx > x else -1
        while y != ty:
            path.append("S" if ty > y else "N")
            y += 1 if ty > y else -1
        return path

    def get_solution_path(self) -> list[str]:
        return self.get_solution()
