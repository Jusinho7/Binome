import math
from collections import defaultdict
from .models import Zone, Connection, DroneMap
from .pathfinding import Pathfinder
from .drone import Drone


class SimulationEngine:
    def __init__(self, drone_map: DroneMap) -> None:
        self.drone_map = drone_map
        self.pathfinder = Pathfinder(drone_map)
        self.drones: list[Drone] = [
            Drone(i + 1, drone_map.start) for i in range(drone_map.nb_drones)
        ]
        self.zone_occupancy: dict[str, int] = defaultdict(int)
        self.zone_occupancy[drone_map.start.name] = len(self.drones)
        self.future_arrivals: dict[int, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.turn_log: list[list[str]] = []
        self._compute_initial_paths()

    def _compute_initial_paths(self) -> None:
        path = self.pathfinder.shortest_path(self.drone_map.start, self.drone_map.end)
        for drone in self.drones:
            drone.set_path(path)

    def _zone_capacity(self, zone: Zone) -> float:
        if zone is self.drone_map.start or zone is self.drone_map.end:
            return math.inf
        return zone.max_drones if zone.max_drones is not None else 1

    def _connection_between(self, a: Zone, b: Zone) -> Connection:
        for conn in self.drone_map.neighbors(a):
            if conn.other(a) is b:
                return conn
        raise ValueError(f"No connection between {a.name} and {b.name}")

    def run(self, max_turns: int = 500) -> list[list[str]]:
        turn = 0
        while not all(d.delivered for d in self.drones):
            turn += 1
            if turn > max_turns:
                raise RuntimeError("Simulation exceeded max_turns — possible deadlock")
            self.turn_log.append(self._simulate_turn(turn))
        return self.turn_log

    def _simulate_turn(self, turn: int) -> list[str]:
        moves: list[str] = []
        connection_usage: dict[str, int] = defaultdict(int)

        for drone in self._active_drones():
            if drone.in_transit and drone.arrival_turn == turn:
                target = drone.transit_target
                self.zone_occupancy[target.name] += 1
                drone.complete_transit()
                moves.append(f"D{drone.id}-{target.name}")
                if target is self.drone_map.end:
                    drone.delivered = True

        for drone in sorted(self._active_drones(), key=lambda d: d.id):
            if drone.in_transit or drone.delivered:
                continue

            next_zone = drone.next_zone()
            if next_zone is None:
                continue

            origin = drone.current_zone
            connection = self._connection_between(origin, next_zone)
            conn_key = f"{origin.name}-{next_zone.name}"

            if connection_usage[conn_key] >= connection.max_link_capacity:
                continue

            if next_zone.zone_type == "restricted":
                arrival_turn = turn + 1
                reserved = self.future_arrivals[arrival_turn][next_zone.name]
                capacity = self._zone_capacity(next_zone)

                if self.zone_occupancy[next_zone.name] + reserved >= capacity:
                    continue

                connection_usage[conn_key] += 1
                self.future_arrivals[arrival_turn][next_zone.name] += 1
                self.zone_occupancy[origin.name] -= 1
                drone.start_transit(next_zone, arrival_turn)
                moves.append(f"D{drone.id}-{conn_key}")
            else:
                capacity = self._zone_capacity(next_zone)
                if self.zone_occupancy[next_zone.name] >= capacity:
                    continue

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