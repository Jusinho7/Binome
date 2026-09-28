"""A* pathfinding helpers for drones with time-based reservations."""

import heapq
import math
from typing import Optional

from models import DroneMap, Zone


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
        self._heuristic_cache: dict[str, dict[str, int]] = {}

    def _heuristic(self, zone: Zone, goal: Zone) -> float:
        """Calculate the Euclidean distance between two zones.

        Args:
            zone: Current zone.
            goal: Destination zone.

        Returns:
            The Euclidean distance between the two zones.
        """
        distances = self._heuristic_cache.get(goal.name)
        if distances is None:
            distances = self._build_heuristic_distances(goal)
            self._heuristic_cache[goal.name] = distances
        return float(distances.get(zone.name, math.inf))

    def _build_heuristic_distances(self, goal: Zone) -> dict[str, int]:
        """Build reverse shortest-path costs without reservations."""
        distances: dict[str, int] = {goal.name: 0}
        frontier: list[tuple[int, str]] = [(0, goal.name)]

        while frontier:
            distance, zone_name = heapq.heappop(frontier)
            if distance != distances[zone_name]:
                continue

            zone = self.drone_map.zones[zone_name]
            for connection in self.drone_map.neighbors(zone):
                previous_zone = connection.other(zone)
                if previous_zone.is_blocked():
                    continue

                candidate = distance + zone.movement_cost()
                if candidate >= distances.get(previous_zone.name, math.inf):
                    continue

                distances[previous_zone.name] = candidate
                heapq.heappush(frontier, (candidate, previous_zone.name))

        return distances

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

    def _congestion_penalty(
        self,
        current_zone: Zone,
        next_zone: Zone,
        departure_turn: int,
        arrival_turn: int,
        zone_reservations: dict[tuple[str, int], int],
        connection_reservations: dict[tuple[str, int], int],
        connection_capacity: int,
    ) -> float:
        """Prefer routes with less previously reserved capacity."""
        zone_capacity = self._zone_capacity(next_zone)
        zone_penalty = 0.0
        if zone_capacity != math.inf:
            zone_usage = zone_reservations.get(
                (next_zone.name, arrival_turn), 0
            )
            zone_penalty = zone_usage / zone_capacity

        connection_penalty = 0.0
        if connection_capacity > 0:
            connection_key = self._connection_key(current_zone, next_zone)
            connection_penalty = sum(
                connection_reservations.get((connection_key, turn), 0)
                / connection_capacity
                for turn in range(departure_turn + 1, arrival_turn + 1)
            )

        return zone_penalty + connection_penalty

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
        if start.is_blocked() or end.is_blocked():
            raise PathNotFoundError(
                f"No valid path found from {start.name} to {end.name}."
            )

        if start is end:
            return [(start, start_turn)]

        start_state = (start.name, start_turn)
        frontier: list[
            tuple[float, int, float, int, int, tuple[str, int]]
        ] = [
            (
                self._heuristic(start, end),
                0,
                0.0,
                0,
                start_turn,
                start_state,
            )
        ]
        previous: dict[tuple[str, int], Optional[tuple[str, int]]] = {
            start_state: None
        }
        best_cost: dict[tuple[str, int], int] = {start_state: 0}
        best_priority_count: dict[tuple[str, int], int] = {start_state: 0}
        best_congestion: dict[tuple[str, int], float] = {start_state: 0.0}
        best_goal_state: Optional[tuple[str, int]] = None
        best_goal_cost = math.inf
        best_goal_rank: Optional[tuple[int, float]] = None

        while frontier:
            (
                estimated_cost,
                negative_priority_count,
                congestion_cost,
                path_cost,
                _,
                state,
            ) = heapq.heappop(frontier)
            priority_count = -negative_priority_count
            if estimated_cost > best_goal_cost:
                break
            if (
                path_cost != best_cost.get(state)
                or priority_count != best_priority_count.get(state)
                or congestion_cost != best_congestion.get(state)
            ):
                continue

            zone_name, turn = state
            current_zone = self.drone_map.zones[zone_name]
            if current_zone is end:
                goal_rank = (-priority_count, congestion_cost)
                if (
                    path_cost < best_goal_cost
                    or (
                        path_cost == best_goal_cost
                        and (
                            best_goal_rank is None
                            or goal_rank < best_goal_rank
                        )
                    )
                ):
                    best_goal_state = state
                    best_goal_cost = path_cost
                    best_goal_rank = goal_rank
                continue

            arrival_turn = turn + 1
            if arrival_turn > max_turn:
                continue

            wait_state = (current_zone.name, arrival_turn)
            current_cost = best_cost[state]
            if current_cost is not None:
                wait_usage = zone_reservations.get(
                    (current_zone.name, arrival_turn), 0
                ) + 1
                if wait_usage <= self._zone_capacity(current_zone):
                    tentative_cost = current_cost + 1
                    existing_cost = best_cost.get(wait_state)
                    wait_rank = (-priority_count, congestion_cost)
                    existing_rank = None
                    if existing_cost is not None:
                        existing_rank = (
                            -best_priority_count[wait_state],
                            best_congestion[wait_state],
                        )
                    if (
                        existing_cost is None
                        or tentative_cost < existing_cost
                        or (
                            tentative_cost == existing_cost
                            and (
                                existing_rank is None
                                or wait_rank < existing_rank
                            )
                        )
                    ):
                        previous[wait_state] = state
                        best_cost[wait_state] = tentative_cost
                        best_priority_count[wait_state] = priority_count
                        best_congestion[wait_state] = congestion_cost
                        estimated_wait_cost = (
                            float(tentative_cost)
                            + self._heuristic(current_zone, end)
                        )
                        heapq.heappush(
                            frontier,
                            (
                                estimated_wait_cost,
                                -priority_count,
                                congestion_cost,
                                tentative_cost,
                                arrival_turn,
                                wait_state,
                            ),
                        )

            for connection in self.drone_map.neighbors(current_zone):
                next_zone = connection.other(current_zone)
                if next_zone.is_blocked():
                    continue

                travel_time = next_zone.movement_cost()
                arrival_turn = turn + travel_time
                if arrival_turn > max_turn:
                    continue

                conn_key = self._connection_key(current_zone, next_zone)
                for transit_turn in range(turn + 1, arrival_turn + 1):
                    connection_usage = (
                        connection_reservations.get(
                            (conn_key, transit_turn), 0
                        )
                        + 1
                    )
                    if connection_usage > connection.max_link_capacity:
                        break
                else:
                    zone_usage = zone_reservations.get(
                        (next_zone.name, arrival_turn), 0
                    ) + 1
                    if zone_usage > self._zone_capacity(next_zone):
                        continue

                    next_state = (next_zone.name, arrival_turn)
                    tentative_cost = current_cost + travel_time
                    next_priority_count = priority_count + int(
                        next_zone.zone_type == "priority"
                    )
                    next_congestion = congestion_cost + (
                        self._congestion_penalty(
                            current_zone,
                            next_zone,
                            turn,
                            arrival_turn,
                            zone_reservations,
                            connection_reservations,
                            connection.max_link_capacity,
                        )
                    )
                    existing_cost = best_cost.get(next_state)
                    next_rank = (-next_priority_count, next_congestion)
                    existing_rank = None
                    if existing_cost is not None:
                        existing_rank = (
                            -best_priority_count[next_state],
                            best_congestion[next_state],
                        )
                    if existing_cost is not None and (
                        tentative_cost > existing_cost
                        or (
                            tentative_cost == existing_cost
                            and existing_rank is not None
                            and next_rank >= existing_rank
                        )
                    ):
                        continue

                    previous[next_state] = state
                    best_cost[next_state] = tentative_cost
                    best_priority_count[next_state] = next_priority_count
                    best_congestion[next_state] = next_congestion
                    estimated_next_cost = (
                        float(tentative_cost)
                        + self._heuristic(next_zone, end)
                    )
                    heapq.heappush(
                        frontier,
                        (
                            estimated_next_cost,
                            -next_priority_count,
                            next_congestion,
                            tentative_cost,
                            arrival_turn,
                            next_state,
                        ),
                    )

        if best_goal_state is not None:
            return self._reconstruct(previous, best_goal_state)

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
