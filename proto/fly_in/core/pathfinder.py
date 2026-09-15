"""Time-expanded pathfinding used to schedule a single drone's route.

Design
------
Each search state is a pair ``(zone_name, turn)`` meaning "the drone is
resting inside ``zone_name`` right after simulation turn ``turn`` has
completed" (``turn == start_turn`` is the initial state, before any turn
has elapsed).

From a state, two kinds of transitions are explored:

* **Wait**: stay in the same zone for one more turn, if the zone still
  has free capacity at the next turn.
* **Move**: travel to a neighboring zone through a connection. The cost
  in turns is dictated by the destination zone type (1 for
  normal/priority, 2 for restricted, and blocked zones are never
  explored). The connection and the destination zone must both have
  free capacity for every turn of the traversal.

A classic Dijkstra search (all edge weights are positive) finds the
earliest turn at which the end zone can be reached while respecting a
shared :class:`~fly_in.core.reservation.ReservationTable`. Because
zones of type ``priority`` should be *preferred* (not merely allowed)
when several routes share the same arrival turn, ties are broken using
a secondary key that rewards routes crossing more priority zones.

This module purposefully avoids any third-party graph/pathfinding
library, as required by the subject.
"""

from __future__ import annotations

import heapq
from typing import Dict, List, Optional, Tuple

from fly_in.core.connection import Connection
from fly_in.core.exceptions import UnreachableDestinationError
from fly_in.core.graph_map import DroneMap
from fly_in.core.reservation import ReservationTable

# A chain link: (turn, zone_name, connection_used_to_arrive_or_None)
ChainLink = Tuple[int, str, Optional[Connection]]


class PathMove:
    """A single committed movement segment of a drone's final schedule."""

    def __init__(
        self,
        departure_turn: int,
        connection: Connection,
        destination_zone: str,
        cost: int,
    ) -> None:
        self.departure_turn = departure_turn
        self.connection = connection
        self.destination_zone = destination_zone
        self.cost = cost

    @property
    def arrival_turn(self) -> int:
        """The turn at which the drone lands in ``destination_zone``."""
        return self.departure_turn + self.cost


class Pathfinder:
    """Computes conflict-free, minimal-turn schedules for a shared map."""

    def __init__(self, drone_map: DroneMap, base_horizon: int = 300) -> None:
        self._map = drone_map
        self._base_horizon = base_horizon

    def find_and_reserve(
        self,
        drone_id: str,
        start_zone: str,
        end_zone: str,
        start_turn: int,
        reservation: ReservationTable,
    ) -> List[PathMove]:
        """Find the earliest-arrival path and commit it to ``reservation``.

        The search horizon grows automatically if the destination cannot
        be reached within the current bound, up to a hard cap.

        Args:
            drone_id: Identifier used only for error reporting.
            start_zone: Name of the zone the drone currently rests in.
            end_zone: Name of the target zone.
            start_turn: The turn at which the drone starts searching
                (0 for a fresh departure, or later for drones queued
                behind others at the start hub).
            reservation: The shared table of already-committed drones.

        Returns:
            The ordered list of :class:`PathMove` segments composing the
            schedule (waits are implicit gaps between segments).

        Raises:
            UnreachableDestinationError: If no path is found even after
                growing the search horizon to its maximum.
        """
        horizon = self._base_horizon
        while horizon <= 5000:
            chain = self._search(start_zone, end_zone, start_turn, horizon, reservation)
            if chain is not None:
                self._commit(chain, reservation)
                return self._to_moves(chain)
            horizon *= 2
        raise UnreachableDestinationError(drone_id)

    # -- internal helpers --------------------------------------------------

    def _search(
        self,
        start_zone: str,
        end_zone: str,
        start_turn: int,
        horizon: int,
        reservation: ReservationTable,
    ) -> Optional[List[ChainLink]]:
        counter = 0
        # heap entries: (turn, negative_priority_bonus, insertion_order, zone_name)
        heap: List[Tuple[int, int, int, str]] = [(start_turn, 0, counter, start_zone)]
        visited: set[Tuple[str, int]] = set()
        best_bonus: Dict[Tuple[str, int], int] = {(start_zone, start_turn): 0}
        prev: Dict[Tuple[str, int], Tuple[str, int, Optional[Connection]]] = {}

        while heap:
            turn, neg_bonus, _, zone_name = heapq.heappop(heap)
            state = (zone_name, turn)
            if state in visited:
                continue
            visited.add(state)

            if zone_name == end_zone:
                return self._reconstruct(prev, start_zone, start_turn, state)

            if turn >= horizon:
                continue

            zone = self._map.get_zone(zone_name)

            # Option A: wait one turn in place.
            next_turn = turn + 1
            if zone.has_unlimited_capacity or reservation.zone_available(
                zone_name, next_turn, zone.max_drones
            ):
                self._offer(
                    heap, best_bonus, prev, counter, next_turn, neg_bonus,
                    zone_name, (zone_name, turn, None),
                )
                counter += 1

            # Option B: move to each reachable neighbor.
            for neighbor_zone, connection in self._map.neighbors(zone_name):
                if not neighbor_zone.zone_type.is_traversable:
                    continue
                cost = neighbor_zone.zone_type.movement_cost
                arrival_turn = turn + cost
                if arrival_turn > horizon:
                    continue
                if not self._connection_free(connection, turn, cost, reservation):
                    continue
                if not (
                    neighbor_zone.has_unlimited_capacity
                    or reservation.zone_available(
                        neighbor_zone.name, arrival_turn, neighbor_zone.max_drones
                    )
                ):
                    continue
                bonus = neg_bonus - (1 if neighbor_zone.zone_type.is_priority else 0)
                self._offer(
                    heap, best_bonus, prev, counter, arrival_turn, bonus,
                    neighbor_zone.name, (zone_name, turn, connection),
                )
                counter += 1

        return None

    @staticmethod
    def _offer(
        heap: List[Tuple[int, int, int, str]],
        best_bonus: Dict[Tuple[str, int], int],
        prev: Dict[Tuple[str, int], Tuple[str, int, Optional[Connection]]],
        counter: int,
        turn: int,
        bonus: int,
        zone_name: str,
        predecessor: Tuple[str, int, Optional[Connection]],
    ) -> None:
        state = (zone_name, turn)
        if state not in best_bonus or bonus < best_bonus[state]:
            best_bonus[state] = bonus
            prev[state] = predecessor
        heapq.heappush(heap, (turn, bonus, counter, zone_name))

    def _connection_free(
        self,
        connection: Connection,
        current_turn: int,
        cost: int,
        reservation: ReservationTable,
    ) -> bool:
        for turn in range(current_turn + 1, current_turn + cost + 1):
            if not reservation.connection_available(
                connection.name, turn, connection.max_link_capacity
            ):
                return False
        return True

    def _reconstruct(
        self,
        prev: Dict[Tuple[str, int], Tuple[str, int, Optional[Connection]]],
        start_zone: str,
        start_turn: int,
        end_state: Tuple[str, int],
    ) -> List[ChainLink]:
        chain: List[ChainLink] = []
        state = end_state
        while state != (start_zone, start_turn):
            zone_name, turn = state
            prev_zone, prev_turn, connection = prev[state]
            chain.append((turn, zone_name, connection))
            state = (prev_zone, prev_turn)
        chain.append((start_turn, start_zone, None))
        chain.reverse()
        return chain

    def _commit(self, chain: List[ChainLink], reservation: ReservationTable) -> None:
        for index, (turn, zone_name, connection) in enumerate(chain):
            zone = self._map.get_zone(zone_name)
            if not zone.has_unlimited_capacity:
                reservation.reserve_zone(zone_name, turn)
            if connection is not None:
                prev_turn = chain[index - 1][0]
                for busy_turn in range(prev_turn + 1, turn + 1):
                    reservation.reserve_connection(connection.name, busy_turn)

    @staticmethod
    def _to_moves(chain: List[ChainLink]) -> List[PathMove]:
        moves: List[PathMove] = []
        for index in range(1, len(chain)):
            turn, zone_name, connection = chain[index]
            if connection is None:
                continue  # a plain wait, no move to record
            prev_turn = chain[index - 1][0]
            moves.append(
                PathMove(
                    departure_turn=prev_turn,
                    connection=connection,
                    destination_zone=zone_name,
                    cost=turn - prev_turn,
                )
            )
        return moves
