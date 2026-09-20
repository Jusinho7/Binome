import heapq
import math
from typing import Optional
from .models import Zone, DroneMap


class PathNotFoundError(Exception):
    pass


class SpaceTimePathfinder:
    def __init__(self, drone_map: DroneMap) -> None:
        self.drone_map = drone_map

    def _heuristic(self, zone: Zone, goal: Zone) -> float:
        return math.hypot(zone.x - goal.x, zone.y - goal.y)

    def _zone_capacity(self, zone: Zone) -> float:
        if zone is self.drone_map.start or zone is self.drone_map.end:
            return math.inf
        return zone.max_drones if zone.max_drones is not None else 1

    @staticmethod
    def _connection_key(zone_a: Zone, zone_b: Zone) -> str:
        """
        Order-independent key so a-b and b-a share the same reservation slot.
        """
        names = sorted([zone_a.name, zone_b.name])
        return f"{names[0]}-{names[1]}"

    def find_path(
        self,
        start: Zone,
        end: Zone,
        zone_reservations: dict[tuple[str, int], int],
        connection_reservations: dict[tuple[str, int], int],
        start_turn: int = 0,
        max_turn: int = 200,
    ) -> list[tuple[Zone, int]]:
        """
        Finds a path as a list of (Zone, turn) pairs,
        avoiding overbooked slots.

        Args:
            zone_reservations:
                maps (zone_name, turn) -> drones already booked there.
            connection_reservations:
                maps (connection_key, turn) -> drones already
                booked traversing that connection during that turn.
        """
        start_state = (start.name, start_turn)
        g_score: dict[tuple[str, int], float] = {start_state: 0.0}
        previous: dict[
            tuple[str, int], Optional[tuple[str, int]]
        ] = {start_state: None}
        visited: set[tuple[str, int]] = set()

        heap: list[tuple[float, int, tuple[str, int]]] = [
            (self._heuristic(start, end), 0, start_state)
        ]
        counter = 1

        while heap:
            _, _, current_state = heapq.heappop(heap)
            if current_state in visited:
                continue
            visited.add(current_state)

            current_name, current_turn = current_state
            if current_name == end.name:
                return self._reconstruct(previous, current_state)

            if current_turn >= max_turn:
                continue

            current_zone = self.drone_map.zones[current_name]

            wait_state = (current_name, current_turn + 1)
            wait_cost = g_score[current_state] + 0.01
            if wait_state not in g_score or wait_cost < g_score[wait_state]:
                g_score[wait_state] = wait_cost
                previous[wait_state] = current_state
                f = wait_cost + self._heuristic(current_zone, end)
                heapq.heappush(heap, (f, counter, wait_state))
                counter += 1

            for connection in self.drone_map.neighbors(current_zone):
                neighbor = connection.other(current_zone)
                if neighbor.is_blocked():
                    continue

                cost = neighbor.movement_cost()
                arrival_turn = current_turn + cost
                neighbor_state = (neighbor.name, arrival_turn)
                conn_key = self._connection_key(current_zone, neighbor)

                zone_occupied = zone_reservations.get(neighbor_state, 0)
                if zone_occupied >= self._zone_capacity(neighbor):
                    continue

                transit_turns = range(current_turn + 1, arrival_turn + 1)
                if any(
                    connection_reservations.get((conn_key, t), 0)
                    >= connection.max_link_capacity
                    for t in transit_turns
                ):
                    continue

                tentative_g = g_score[current_state] + cost
                if (
                    neighbor_state not in g_score
                    or tentative_g < g_score[neighbor_state]
                ):
                    g_score[neighbor_state] = tentative_g
                    previous[neighbor_state] = current_state
                    f = tentative_g + self._heuristic(neighbor, end)
                    heapq.heappush(heap, (f, counter, neighbor_state))
                    counter += 1

        raise PathNotFoundError(
            f"No time-respecting path found from "
            f"'{start.name}' to '{end.name}'"
        )

    def _reconstruct(
        self,
        previous: dict[tuple[str, int], Optional[tuple[str, int]]],
        end_state: tuple[str, int],
    ) -> list[tuple[Zone, int]]:
        path: list[tuple[str, int]] = []
        current: Optional[tuple[str, int]] = end_state
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()
        return [(self.drone_map.zones[name], turn) for name, turn in path]


class Pathfinder(SpaceTimePathfinder):
    def shortest_path(self, start: Zone, end: Zone) -> list[Zone]:
        timed_path = self.find_path(
            start,
            end,
            zone_reservations={},
            connection_reservations={},
        )
        return [zone for zone, _ in timed_path]
