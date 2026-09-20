"""A* pathfinding helpers for drones with time-based reservations."""

import heapq
import math
from typing import Optional

from .models import DroneMap, Zone


class PathNotFoundError(Exception):
    """Raised when no valid path can be found."""


class SpaceTimePathfinder:
    """Find paths while considering time-based zone reservations."""

    def __init__(self, drone_map: DroneMap) -> None:
        """Initialize the pathfinder with a drone map.

        Args:
            drone_map: Map containing zones and their connections.
        """
        self.drone_map = drone_map

    def _heuristic(self, zone: Zone, goal: Zone) -> float:
        """Calculate the Euclidean distance between two zones.

        Args:
            zone: Current zone.
            goal: Destination zone.

        Returns:
            The Euclidean distance between the two zones.
        """
        return math.hypot(zone.x - goal.x, zone.y - goal.y)

    def _zone_capacity(self, zone: Zone) -> float:
        """Return the maximum number of drones allowed in a zone.

        Args:
            zone: Zone whose capacity should be determined.

        Returns:
            The zone capacity. Start and end zones have unlimited capacity.
        """
        if zone is self.drone_map.start or zone is self.drone_map.end:
            return math.inf
        return zone.max_drones if zone.max_drones is not None else 1

    @staticmethod
    def _connection_key(zone_a: Zone, zone_b: Zone) -> str:
        """Create an order-independent key for a connection.

        Args:
            zone_a: First zone of the connection.
            zone_b: Second zone of the connection.

        Returns:
            A connection key shared by both directions.
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
        """Find a path while respecting time-based reservations.

        Args:
            start: Starting zone.
            end: Destination zone.
            zone_reservations: Drones already booked in each zone and turn.
            connection_reservations: Drones already using each
                connection during each turn.
            start_turn: Turn at which the path search begins.
            max_turn: Maximum turn allowed for the search.

        Returns:
            A list of ``(Zone, turn)`` pairs describing the path.

        Raises:
            PathNotFoundError: If no valid path can be found.
        """
        if start is end:
            return [(start, start_turn)]

        start_state = (start.name, start_turn)
        frontier: list[tuple[float, int, int, tuple[str, int]]] = [
            (self._heuristic(start, end), 0, start_turn, start_state)
        ]
        previous: dict[tuple[str, int], Optional[tuple[str, int]]] = {
            start_state: None
        }
        best_cost: dict[tuple[str, int], int] = {start_state: 0}

        while frontier:
            _, _, _, state = heapq.heappop(frontier)
            zone_name, turn = state
            current_zone = self.drone_map.zones[zone_name]
            if current_zone is end:
                return self._reconstruct(previous, state)

            arrival_turn = turn + 1
            if arrival_turn > max_turn:
                continue

            wait_state = (current_zone.name, arrival_turn)
            current_cost = best_cost.get(state)
            if current_cost is not None:
                wait_usage = zone_reservations.get(
                    (current_zone.name, arrival_turn), 0
                ) + 1
                if wait_usage <= self._zone_capacity(current_zone):
                    tentative_cost = current_cost + 1
                    existing_cost = best_cost.get(wait_state)
                    if existing_cost is None or tentative_cost < existing_cost:
                        previous[wait_state] = state
                        best_cost[wait_state] = tentative_cost
                        priority = float(tentative_cost) + self._heuristic(
                            current_zone, end
                        )
                        heapq.heappush(
                            frontier,
                            (
                                priority,
                                tentative_cost,
                                arrival_turn,
                                wait_state,
                            ),
                        )

            for connection in self.drone_map.neighbors(current_zone):
                next_zone = connection.other(current_zone)
                conn_key = self._connection_key(current_zone, next_zone)
                connection_usage = (
                    connection_reservations.get((conn_key, arrival_turn), 0)
                    + 1
                )
                if connection_usage > connection.max_link_capacity:
                    continue

                zone_usage = zone_reservations.get(
                    (next_zone.name, arrival_turn), 0
                ) + 1
                if zone_usage > self._zone_capacity(next_zone):
                    continue

                next_state = (next_zone.name, arrival_turn)
                current_cost = best_cost.get(state)
                if current_cost is None:
                    continue

                tentative_cost = current_cost + 1
                existing_cost = best_cost.get(next_state)
                if (
                    existing_cost is not None
                    and tentative_cost >= existing_cost
                ):
                    continue

                previous[next_state] = state
                best_cost[next_state] = tentative_cost
                priority = float(tentative_cost) + self._heuristic(
                    next_zone, end
                )
                heapq.heappush(
                    frontier,
                    (priority, tentative_cost, arrival_turn, next_state),
                )

        raise PathNotFoundError(
            f"No valid path found from {start.name} to {end.name}."
        )

    def _reconstruct(
        self,
        previous: dict[tuple[str, int], Optional[tuple[str, int]]],
        end_state: tuple[str, int],
    ) -> list[tuple[Zone, int]]:
        """Reconstruct the path from the predecessor states.

        Args:
            previous: Mapping of each state to its predecessor.
            end_state: Final state of the path.

        Returns:
            The reconstructed path as ``(Zone, turn)`` pairs.
        """
        path: list[tuple[str, int]] = []
        current: Optional[tuple[str, int]] = end_state
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()
        return [(self.drone_map.zones[name], turn) for name, turn in path]


class Pathfinder(SpaceTimePathfinder):
    """Provide a simplified interface for shortest-path searches."""

    def shortest_path(self, start: Zone, end: Zone) -> list[Zone]:
        """Find the shortest path between two zones.

        Args:
            start: Starting zone.
            end: Destination zone.

        Returns:
            A list of zones forming the shortest path.
        """
        timed_path = self.find_path(
            start,
            end,
            zone_reservations={},
            connection_reservations={},
        )
        return [zone for zone, _ in timed_path]
