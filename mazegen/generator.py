import random
from collections import deque
from typing import Optional
from .pattern42 import PATTERN_42, PATTERN_HEIGHT, PATTERN_WIDTH

NORTH, EAST, SOUTH, WEST = "N", "E", "S", "W"

_DIRECTIONS: dict[str, tuple[int, int, int]] = {
    NORTH: (0, -1, 0b0001),
    EAST: (1, 0, 0b0010),
    SOUTH: (0, 1, 0b0100),
    WEST: (-1, 0, 0b1000),
}

_OPPOSITE: dict[str, str] = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}

FULLY_CLOSED = 0b1111


class MazeGenerationError(Exception): ...


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        seed: Optional[int] = None,
        perfect: bool = True,
        entry: tuple[int, int] = (0, 0),
        exit: tuple[int, int] = (0, 0),
        embed_pattern: bool = True,
    ) -> None:
        if width < 1 or height < 1:
            raise MazeGenerationError("width and height must be >= 1")
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self.entry = entry
        self.exit = exit
        self.embed_pattern = embed_pattern
        self._rng = random.Random(seed)
        self._walls: list[list[int]] = [
            [FULLY_CLOSED for _ in range(width)] for _ in range(height)
        ]
        self._pattern_cells: set[tuple[int, int]] = set()
        self._generated = False
        self.pattern_warning: Optional[str] = None

    def generate(self) -> None:
        self._validate_entry_exit()
        self._place_pattern()
        self._carve_spanning_tree()
        if not self.perfect:
            self._add_loops()
        self._generated = True

    def get_walls(self) -> list[list[int]]:
        """Return walls."""
        self._ensure_generated()
        return [row[:] for row in self._walls]

    def get_pattern_cells(self) -> set[tuple[int, int]]:
        """returns the cell with 42 pattern."""
        return set(self._pattern_cells)

    def shortest_path(
        self,
        start: Optional[tuple[int, int]] = None,
        end: Optional[tuple[int, int]] = None,
    ) -> str:
        self._ensure_generated()
        start = start or self.entry
        end = end or self.exit
        if start == end:
            return ""

        prev: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}
        visited = {start}
        queue: deque[tuple[int, int]] = deque([start])
        while queue:
            cur = queue.popleft()
            if cur == end:
                break
            x, y = cur
            for direction, (dx, dy, bit) in _DIRECTIONS.items():
                if self._walls[y][x] & bit:
                    continue
                nxt = (x + dx, y + dy)
                if nxt in visited:
                    continue
                visited.add(nxt)
                prev[nxt] = (cur, direction)
                queue.append(nxt)
        else:
            raise MazeGenerationError("no path between start and end")

        path: list[str] = []
        node = end
        while node != start:
            parent, direction = prev[node]
            path.append(direction)
            node = parent
        path.reverse()
        return "".join(path)

    def _ensure_generated(self) -> None:
        if not self._generated:
            raise MazeGenerationError("generate() must be called first")

    def _in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def _validate_entry_exit(self) -> None:
        for name, (x, y) in (("entry", self.entry), ("exit", self.exit)):
            if not self._in_bounds(x, y):
                raise MazeGenerationError(f"{name} {(x, y)} is out of bounds")
        if self.entry == self.exit:
            raise MazeGenerationError("entry and exit must be different")

    def _place_pattern(self) -> None:
        """Reserve cells to put it "42", if the maze is large enough."""
        if not self.embed_pattern:
            return
        margin = 1
        needed_w = PATTERN_WIDTH + margin * 2
        needed_h = PATTERN_HEIGHT + margin * 2
        if self.width < needed_w or self.height < needed_h:
            self.pattern_warning = (
                "Maze too small to embed the '42' pattern "
                f"(needs at least {needed_w}x{needed_h})."
            )
            print(f"[warning] {self.pattern_warning}")
            return

        ox = (self.width - PATTERN_WIDTH) // 2
        oy = (self.height - PATTERN_HEIGHT) // 2
        candidate: set[tuple[int, int]] = set()
        for row_idx, row in enumerate(PATTERN_42):
            for col_idx, ch in enumerate(row):
                if ch == "1":
                    candidate.add((ox + col_idx, oy + row_idx))

        # Never let the pattern swallow the entry/exit cells.
        if self.entry in candidate or self.exit in candidate:
            self.pattern_warning = (
                "Entry/exit collide with the '42' pattern; pattern skipped."
            )
            print(f"[warning] {self.pattern_warning}")
            return

        self._pattern_cells = candidate

    def _carve_spanning_tree(self) -> None:
        """Recursive-backtracker (iterative) carve over the free cells."""
        free_cells = {
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if (x, y) not in self._pattern_cells
        }
        if not free_cells:
            raise MazeGenerationError("no free cells to carve a maze into")

        start = (
            self.entry if self.entry in free_cells else next(iter(free_cells))
        )
        visited = {start}
        stack = [start]

        while stack:
            x, y = stack[-1]
            neighbors = []
            for direction, (dx, dy, _bit) in _DIRECTIONS.items():
                nxt = (x + dx, y + dy)
                if nxt in free_cells and nxt not in visited:
                    neighbors.append((direction, nxt))
            if not neighbors:
                stack.pop()
                continue
            direction, nxt = self._rng.choice(neighbors)
            self._open_wall((x, y), direction)
            visited.add(nxt)
            stack.append(nxt)

        unreached = free_cells - visited
        if unreached:
            # Should not normally happen; guard against disconnected areas.
            raise MazeGenerationError(
                f"{len(unreached)} cell(s) unreachable from entry"
            )

    def _open_wall(self, cell: tuple[int, int], direction: str) -> None:
        x, y = cell
        dx, dy, bit = _DIRECTIONS[direction]
        nx, ny = x + dx, y + dy
        self._walls[y][x] &= ~bit
        opp_bit = _DIRECTIONS[_OPPOSITE[direction]][2]
        self._walls[ny][nx] &= ~opp_bit

    def _wall_open(self, x: int, y: int, direction: str) -> bool:
        _dx, _dy, bit = _DIRECTIONS[direction]
        return not (self._walls[y][x] & bit)

    def _creates_3x3_open_area(self, tx: int, ty: int) -> bool:
        """Check every 3x3 window overlapping (tx, ty) for full openness."""
        for oy in range(ty - 2, ty + 1):
            for ox in range(tx - 2, tx + 1):
                if ox < 0 or oy < 0:
                    continue
                if ox + 2 >= self.width or oy + 2 >= self.height:
                    continue
                if self._window_fully_open(ox, oy):
                    return True
        return False

    def _window_fully_open(self, ox: int, oy: int) -> bool:
        for row in range(3):
            for col in range(2):
                x, y = ox + col, oy + row
                if not self._wall_open(x, y, EAST):
                    return False
        for col in range(3):
            for row in range(2):
                x, y = ox + col, oy + row
                if not self._wall_open(x, y, SOUTH):
                    return False
        return True

    def _add_loops(self, extra_ratio: float = 0.12) -> None:
        """Randomly open a few extra walls to break perfection.

        Skips any candidate that would create a >=3x3 fully-open area, and
        never touches pattern cells.
        """
        candidates: list[tuple[tuple[int, int], str]] = []
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self._pattern_cells:
                    continue
                for direction, (dx, dy, _bit) in _DIRECTIONS.items():
                    nx, ny = x + dx, y + dy
                    if not self._in_bounds(nx, ny):
                        continue
                    if (nx, ny) in self._pattern_cells:
                        continue
                    if not self._wall_open(x, y, direction):
                        candidates.append(((x, y), direction))
        self._rng.shuffle(candidates)

        target = int(len(candidates) * extra_ratio)
        opened = 0
        for (x, y), direction in candidates:
            if opened >= target:
                break
            if self._wall_open(x, y, direction):
                continue  # already opened by a previous iteration
            dx, dy, _bit = _DIRECTIONS[direction]
            nx, ny = x + dx, y + dy
            self._open_wall((x, y), direction)
            creates_room = self._creates_3x3_open_area(
                x, y
            ) or self._creates_3x3_open_area(nx, ny)
            if creates_room:
                self._close_wall((x, y), direction)
            else:
                opened += 1

    def _close_wall(self, cell: tuple[int, int], direction: str) -> None:
        x, y = cell
        dx, dy, bit = _DIRECTIONS[direction]
        nx, ny = x + dx, y + dy
        self._walls[y][x] |= bit
        opp_bit = _DIRECTIONS[_OPPOSITE[direction]][2]
        self._walls[ny][nx] |= opp_bit
