import heapq
import math
from typing import Optional
from .models import Zone, DroneMap


class PathNotFoundError(Exception):
    pass


class Pathfinder:
    def __init__(self, drone_map: DroneMap) -> None:
        self.drone_map = drone_map

    def _heuristic(self, zone: Zone, goal: Zone) -> float:
        return math.hypot(zone.x - goal.x, zone.y - goal.y)

    def shortest_path(self, start: Zone, end: Zone) -> list[Zone]:
        g_score: dict[str, float] = {start.name: 0.0}
        previous: dict[str, Optional[str]] = {start.name: None}
        visited: set[str] = set()

        heap: list[tuple[float, int, str]] = [(self._heuristic(start, end), 0, start.name)]
        counter = 1

        while heap:
            _, _, current_name = heapq.heappop(heap)

            if current_name in visited:
                continue
            visited.add(current_name)

            if current_name == end.name:
                break

            current_zone = self.drone_map.zones[current_name]

            for connection in self.drone_map.neighbors(current_zone):
                neighbor = connection.other(current_zone)

                if neighbor.is_blocked() or neighbor.name in visited:
                    continue

                tentative_g = g_score[current_name] + neighbor.movement_cost()

                if neighbor.name not in g_score or tentative_g < g_score[neighbor.name]:
                    g_score[neighbor.name] = tentative_g
                    previous[neighbor.name] = current_name
                    f_score = tentative_g + self._heuristic(neighbor, end)
                    heapq.heappush(heap, (f_score, counter, neighbor.name))
                    counter += 1

        if end.name not in g_score:
            raise PathNotFoundError(f"No path found from '{start.name}' to '{end.name}'")

        return self._reconstruct_path(previous, start.name, end.name)

    def _reconstruct_path(
        self, previous: dict[str, Optional[str]], start_name: str, end_name: str
    ) -> list[Zone]:
        path_names: list[str] = []
        current: Optional[str] = end_name

        while current is not None:
            path_names.append(current)
            current = previous[current]

        path_names.reverse()
        return [self.drone_map.zones[name] for name in path_names]