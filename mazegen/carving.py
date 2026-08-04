"""Maze carving: recursive-backtracker spanning tree and optional loops."""
import random
from .directions import DIRECTIONS, OPPOSITE
from .exceptions import MazeGenerationError


def open_wall(
        walls: list[list[int]],
        cell: tuple[int, int],
        direction: str
) -> None:
    """Open the wall between a cell and its adjacent neighbor."""
    x, y = cell
    dx, dy, bit = DIRECTIONS[direction]
    nx, ny = x + dx, y + dy
    walls[y][x] &= ~bit
    opp_bit = DIRECTIONS[OPPOSITE[direction]][2]
    walls[ny][nx] &= ~opp_bit


def close_wall(
        walls: list[list[int]],
        cell: tuple[int, int],
        direction: str
) -> None:
    """Close the wall between a cell and its adjacent neighbor."""
    x, y = cell
    dx, dy, bit = DIRECTIONS[direction]
    nx, ny = x + dx, y + dy
    walls[y][x] |= bit
    opp_bit = DIRECTIONS[OPPOSITE[direction]][2]
    walls[ny][nx] |= opp_bit


def wall_open(walls: list[list[int]], x: int, y: int, direction: str) -> bool:
    """Return whether the wall in the given direction is open."""
    _dx, _dy, bit = DIRECTIONS[direction]
    return not (walls[y][x] & bit)


def carve_spanning_tree(
    walls: list[list[int]],
    width: int,
    height: int,
    entry: tuple[int, int],
    pattern_cells: set[tuple[int, int]],
    rng: random.Random,
) -> None:
    """Carve a spanning tree using an iterative recursive backtracker."""
    free_cells = {
        (x, y)
        for y in range(height)
        for x in range(width)
        if (x, y) not in pattern_cells
    }
    if not free_cells:
        raise MazeGenerationError("no free cells to carve a maze into")

    start = entry if entry in free_cells else next(iter(free_cells))
    visited = {start}
    stack = [start]

    while stack:
        x, y = stack[-1]
        neighbors = []
        for direction, (dx, dy, _bit) in DIRECTIONS.items():
            nxt = (x + dx, y + dy)
            if nxt in free_cells and nxt not in visited:
                neighbors.append((direction, nxt))
        if not neighbors:
            stack.pop()
            continue
        direction, nxt = rng.choice(neighbors)
        open_wall(walls, (x, y), direction)
        visited.add(nxt)
        stack.append(nxt)

    unreached = free_cells - visited
    if unreached:
        raise MazeGenerationError(
            f"{len(unreached)} cell(s) unreachable from entry"
        )


def _creates_3x3_open_area(
    walls: list[list[int]], width: int, height: int, tx: int, ty: int
) -> bool:
    """Check every 3x3 window overlapping (tx, ty) for full openness."""
    for oy in range(ty - 2, ty + 1):
        for ox in range(tx - 2, tx + 1):
            if ox < 0 or oy < 0:
                continue
            if ox + 2 >= width or oy + 2 >= height:
                continue
            if _window_fully_open(walls, ox, oy):
                return True
    return False


def _window_fully_open(walls: list[list[int]], ox: int, oy: int) -> bool:
    for row in range(3):
        for col in range(2):
            x, y = ox + col, oy + row
            if not wall_open(walls, x, y, "E"):
                return False
    for col in range(3):
        for row in range(2):
            x, y = ox + col, oy + row
            if not wall_open(walls, x, y, "S"):
                return False
    return True


def add_loops(
    walls: list[list[int]],
    width: int,
    height: int,
    pattern_cells: set[tuple[int, int]],
    rng: random.Random,
    extra_ratio: float = 0.12,
) -> None:
    """Randomly open a few extra walls to break perfection.

    Skips any candidate that would create a >=3x3 fully-open area, and
    never touches pattern cells.
    """
    def in_bounds(x: int, y: int) -> bool:
        return 0 <= x < width and 0 <= y < height

    candidates: list[tuple[tuple[int, int], str]] = []
    for y in range(height):
        for x in range(width):
            if (x, y) in pattern_cells:
                continue
            for direction, (dx, dy, _bit) in DIRECTIONS.items():
                nx, ny = x + dx, y + dy
                if not in_bounds(nx, ny):
                    continue
                if (nx, ny) in pattern_cells:
                    continue
                if not wall_open(walls, x, y, direction):
                    candidates.append(((x, y), direction))
    rng.shuffle(candidates)

    target = int(len(candidates) * extra_ratio)
    opened = 0
    for (x, y), direction in candidates:
        if opened >= target:
            break
        if wall_open(walls, x, y, direction):
            continue
        dx, dy, _bit = DIRECTIONS[direction]
        nx, ny = x + dx, y + dy
        open_wall(walls, (x, y), direction)
        creates_room = _creates_3x3_open_area(
            walls, width, height, x, y
        ) or _creates_3x3_open_area(walls, width, height, nx, ny)
        if creates_room:
            close_wall(walls, (x, y), direction)
        else:
            opened += 1
