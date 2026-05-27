# mazegen/solver.py
from typing import List, Tuple, Optional, Dict
from .generator import MazeGenerator


def solve(
    maze: MazeGenerator,
    entry: Tuple[int, int],
    exit: Tuple[int, int],
) -> Optional[List[str]]:
    queue = [entry]
    visited: Dict[Tuple[int, int], Optional[Tuple]] = {entry: None}

    dir_name = {
        MazeGenerator.NORTH: "N",
        MazeGenerator.EAST:  "E",
        MazeGenerator.SOUTH: "S",
        MazeGenerator.WEST:  "W",
    }

    while queue:
        current = queue.pop(0)
        cx, cy = current

        if current == exit:
            return _reconstruct(visited, entry, exit)

        for direction, name in dir_name.items():
            cell = maze.grid[cy][cx]

            if cell & direction:
                continue

            dx, dy = MazeGenerator.DELTA[direction]
            nx, ny = cx + dx, cy + dy

            neighbor = (nx, ny)
            if neighbor not in visited:
                visited[neighbor] = (current, name)
                queue.append(neighbor)

    return None


def _reconstruct(
    visited: Dict,
    entry: Tuple[int, int],
    exit: Tuple[int, int],
) -> List[str]:
    path = []
    current = exit

    while visited[current] is not None:
        prev, direction = visited[current]
        path.append(direction)
        current = prev

    path.reverse()
    return path