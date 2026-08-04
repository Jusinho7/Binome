"""Compute shortest paths through a maze using breadth-first search."""

from collections import deque
from .directions import DIRECTIONS
from .exceptions import MazeGenerationError


def shortest_path(
    walls: list[list[int]],
    start: tuple[int, int],
    end: tuple[int, int],
) -> str:
    """Return the shortest path between two cells.

    Use breadth-first search to guarantee the shortest path.
    """
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
        for direction, (dx, dy, bit) in DIRECTIONS.items():
            if walls[y][x] & bit:
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
