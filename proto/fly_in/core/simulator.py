"""Simulation engine: schedules every drone and builds the turn-by-turn log.

The engine relies on *prioritized planning*: drones are scheduled one
after another (in ID order), each one running a full time-expanded
Dijkstra search (see :mod:`fly_in.core.pathfinder`) against a shared
:class:`~fly_in.core.reservation.ReservationTable` that already holds
every previously scheduled drone's route. This keeps the algorithm
simple, deterministic and easy to reason about, at the cost of not
being a globally optimal multi-agent solution (see the README for a
discussion of this trade-off).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from fly_in.core.drone import Drone, DroneStatus
from fly_in.core.graph_map import DroneMap
from fly_in.core.pathfinder import Pathfinder, PathMove
from fly_in.core.reservation import ReservationTable


@dataclass
class TurnLog:
    """All drone movements that occurred during a single simulation turn."""

    turn: int
    actions: List[str] = field(default_factory=list)

    def render(self) -> str:
        """Render this turn as a single space-separated output line."""
        return " ".join(self.actions)


@dataclass
class SimulationResult:
    """The full outcome of a simulation run."""

    turns: List[TurnLog]
    total_turns: int
    drones_delivered: int
    total_path_cost: int

    @property
    def average_turns_per_drone(self) -> float:
        """Average number of turns each drone spent travelling."""
        if self.drones_delivered == 0:
            return 0.0
        return self.total_path_cost / self.drones_delivered

    def render(self) -> str:
        """Render the full simulation log, one line per turn."""
        return "\n".join(turn.render() for turn in self.turns if turn.actions)


class Simulator:
    """Plans every drone's route and produces the simulation output."""

    def __init__(self, drone_map: DroneMap) -> None:
        self._map = drone_map
        self._pathfinder = Pathfinder(drone_map)

    def run(self) -> SimulationResult:
        """Run the full simulation for every drone declared on the map.

        Returns:
            A :class:`SimulationResult` describing every turn and a few
            aggregate performance metrics.
        """
        reservation = ReservationTable()
        drones: List[Drone] = [
            Drone(drone_id, self._map.start_zone_name)
            for drone_id in range(1, self._map.nb_drones + 1)
        ]

        per_turn_actions: Dict[int, List[tuple[int, str]]] = {}
        max_turn = 0
        total_path_cost = 0

        for drone in drones:
            moves: List[PathMove] = self._pathfinder.find_and_reserve(
                drone_id=drone.label,
                start_zone=self._map.start_zone_name,
                end_zone=self._map.end_zone_name,
                start_turn=0,
                reservation=reservation,
            )
            drone.status = DroneStatus.IN_TRANSIT if moves else DroneStatus.DELIVERED

            for move in moves:
                total_path_cost += move.cost
                for turn in range(move.departure_turn + 1, move.arrival_turn + 1):
                    label = (
                        move.connection.name
                        if turn < move.arrival_turn
                        else move.destination_zone
                    )
                    per_turn_actions.setdefault(turn, []).append(
                        (drone.drone_id, f"{drone.label}-{label}")
                    )
                    max_turn = max(max_turn, turn)

            if moves:
                drone.current_zone = moves[-1].destination_zone
                drone.planned_path = [self._map.start_zone_name] + [
                    move.destination_zone for move in moves
                ]
            drone.deliver()

        turn_logs = [
            TurnLog(
                turn=turn,
                actions=[
                    label
                    for _, label in sorted(per_turn_actions.get(turn, []))
                ],
            )
            for turn in range(1, max_turn + 1)
        ]

        return SimulationResult(
            turns=turn_logs,
            total_turns=max_turn,
            drones_delivered=len(drones),
            total_path_cost=total_path_cost,
        )
