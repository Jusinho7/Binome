"""Drone simulation engine with time-based movement and capacity management."""

import math
from collections import defaultdict
from .drone import Drone
from .models import Connection, DroneMap, Zone
from .pathfinding import Pathfinder


class SimulationEngine:
    """Manage the drone simulation and its time-based movement logic.

    Attributes:
        drone_map: The map containing zones and connections.
        pathfinder: Pathfinder instance for computing paths.
        drones: List of Drone instances in the simulation.
        zone_occupancy: Tracks the number of drones in each zone.
        future_arrivals: Tracks reserved arrivals for future turns.
        active_transits: Tracks connections currently occupied by
            drones in transit.
        turn_log: Records the moves made by drones each turn.
        position_history: Records the positions of all drones at each turn.
    """

    def __init__(self, drone_map: DroneMap) -> None:
        """Initialize the simulation engine with a drone map."""
        self.drone_map = drone_map
        start_zone = drone_map.start
        if start_zone is None:
            raise ValueError("Drone map must define a start zone")

        self.pathfinder = Pathfinder(drone_map)
        self.drones: list[Drone] = [
            Drone(i + 1, start_zone) for i in range(drone_map.nb_drones)
        ]

        self.zone_occupancy: dict[str, int] = defaultdict(int)
        self.zone_occupancy[start_zone.name] = len(self.drones)

        self.future_arrivals: dict[int, dict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        self.active_transits: dict[str, int] = defaultdict(int)

        self.turn_log: list[list[str]] = []
        self.position_history: list[dict[int, Zone]] = []
        self.transit_history: list[
            dict[int, tuple[Zone, Zone, int]]
        ] = []

        self._compute_initial_paths()
        self._save_positions(0)

    def _compute_initial_paths(self) -> None:
        """Compute and reserve initial paths for all drones."""
        start = self.drone_map.start
        end = self.drone_map.end
        if start is None or end is None:
            raise ValueError("Drone map must define both start and end zones")

        zone_reservations: dict[tuple[str, int], int] = {}
        connection_reservations: dict[tuple[str, int], int] = {}

        for drone in self.drones:
            timed_path = self.pathfinder.find_path(
                start, end, zone_reservations, connection_reservations
            )
            plain_path = [zone for zone, _ in timed_path]
            drone.set_path(plain_path)
            self._reserve_timed_path(
                timed_path, zone_reservations, connection_reservations
            )

    def _zone_capacity(self, zone: Zone) -> float:
        """Return the maximum number of drones allowed in a zone."""
        if zone is self.drone_map.start or zone is self.drone_map.end:
            return math.inf
        return zone.max_drones if zone.max_drones is not None else 1

    @staticmethod
    def _connection_key(a: Zone, b: Zone) -> str:
        """Return an order-independent key for a connection."""
        names = sorted([a.name, b.name])
        return f"{names[0]}-{names[1]}"

    def _connection_between(self, a: Zone, b: Zone) -> Connection:
        """Return the connection between two zones."""
        for conn in self.drone_map.neighbors(a):
            if conn.other(a) is b:
                return conn
        raise ValueError(f"No connection between {a.name} and {b.name}")

    def run(self, max_turns: int = 500) -> list[list[str]]:
        """Run the simulation until all drones are delivered."""
        turn = 0
        while not all(d.delivered for d in self.drones):
            turn += 1
            if turn > max_turns:
                raise RuntimeError(
                    "Simulation exceeded max_turns — possible deadlock"
                )
            self.turn_log.append(self._simulate_turn(turn))
            self._save_positions(turn)
        return self.turn_log

    def _save_positions(self, turn: int) -> None:
        """Save the current position of every drone."""
        self.position_history.append(
            {drone.id: drone.current_zone for drone in self.drones}
        )
        self.transit_history.append(
            {
                drone.id: (
                    drone.current_zone,
                    drone.transit_target,
                    drone.arrival_turn,
                )
                for drone in self.drones
                if drone.in_transit
                and drone.transit_target is not None
                and drone.arrival_turn is not None
            }
        )

    def _simulate_turn(self, turn: int) -> list[str]:
        """Simulate one turn and return the resulting drone movements."""
        moves: list[str] = []
        connection_usage: dict[str, int] = defaultdict(int)
        moved_this_turn: set[int] = set()

        for drone in self._active_drones():
            if drone.in_transit and drone.arrival_turn == turn:
                target = drone.transit_target
                if target is None:
                    continue

                origin = drone.current_zone
                conn_key = self._connection_key(origin, target)
                self.active_transits[conn_key] -= 1

                self.zone_occupancy[target.name] += 1
                drone.complete_transit()
                moves.append(f"D{drone.id}-{target.name}")
                moved_this_turn.add(drone.id)
                if target is self.drone_map.end:
                    drone.delivered = True

        for drone in sorted(self._active_drones(), key=lambda d: d.id):
            if drone.id in moved_this_turn:
                continue
            if drone.in_transit or drone.delivered:
                continue

            next_zone = drone.next_zone()
            if next_zone is None:
                continue

            origin = drone.current_zone
            if next_zone is origin:
                drone.path_index += 1
                moves.append(f"D{drone.id}-wait")
                continue

            connection = self._connection_between(origin, next_zone)
            conn_key = self._connection_key(origin, next_zone)

            total_connection_usage = (
                connection_usage[conn_key] + self.active_transits[conn_key]
            )
            if total_connection_usage >= connection.max_link_capacity:
                continue

            if next_zone.zone_type == "restricted":
                arrival_turn = turn + next_zone.movement_cost() - 1
                reserved = self.future_arrivals[arrival_turn][next_zone.name]
                capacity = self._zone_capacity(next_zone)

                if self.zone_occupancy[next_zone.name] + reserved >= capacity:
                    continue

                connection_usage[conn_key] += 1
                self.active_transits[conn_key] += 1
                self.future_arrivals[arrival_turn][next_zone.name] += 1
                self.zone_occupancy[origin.name] -= 1
                drone.start_transit(next_zone, arrival_turn)
                moves.append(f"D{drone.id}-{conn_key}")
            else:
                capacity = self._zone_capacity(next_zone)
                if self.zone_occupancy[next_zone.name] >= capacity:
                    continue  # zone pleine, on attend

                connection_usage[conn_key] += 1
                self.zone_occupancy[origin.name] -= 1
                self.zone_occupancy[next_zone.name] += 1
                drone.advance_direct(next_zone)
                moves.append(f"D{drone.id}-{next_zone.name}")
                if next_zone is self.drone_map.end:
                    drone.delivered = True

        return moves

    def _active_drones(self) -> list[Drone]:
        return [d for d in self.drones if not d.delivered]

    def _reserve_timed_path(
        self,
        timed_path: list[tuple[Zone, int]],
        zone_reservations: dict[tuple[str, int], int],
        connection_reservations: dict[tuple[str, int], int],
    ) -> None:
        """Mark the zones and links used by this path as reserved."""
        for zone, turn in timed_path:
            key = (zone.name, turn)
            zone_reservations[key] = zone_reservations.get(key, 0) + 1

        for (
            (zone_a, turn_a),
            (zone_b, turn_b),
        ) in zip(timed_path, timed_path[1:]):
            if zone_a is zone_b:
                continue
            conn_key = self._connection_key(zone_a, zone_b)
            for t in range(turn_a + 1, turn_b + 1):
                key = (conn_key, t)
                connection_reservations[key] = (
                    connection_reservations.get(key, 0) + 1
                )