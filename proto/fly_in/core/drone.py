"""Drone model and its lifecycle status."""

from __future__ import annotations

from enum import Enum, auto
from typing import List


class DroneStatus(Enum):
    """Lifecycle status of a drone during the simulation."""

    WAITING = auto()
    IN_TRANSIT = auto()
    DELIVERED = auto()


class Drone:
    """A single autonomous drone travelling through the network.

    Attributes:
        drone_id: Unique numeric identifier (1-indexed).
        current_zone: Name of the zone the drone currently rests in, or
            ``None`` while mid-flight over a restricted connection.
        status: Current :class:`DroneStatus`.
        planned_path: Ordered list of zone names computed by the
            pathfinder, from the start zone to the end zone (inclusive).
    """

    def __init__(self, drone_id: int, start_zone: str) -> None:
        self.drone_id = drone_id
        self.current_zone: str = start_zone
        self.status: DroneStatus = DroneStatus.WAITING
        self.planned_path: List[str] = [start_zone]

    @property
    def label(self) -> str:
        """The display identifier used in simulation output, e.g. ``D3``."""
        return f"D{self.drone_id}"

    def deliver(self) -> None:
        """Mark this drone as having reached the end zone."""
        self.status = DroneStatus.DELIVERED

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return (
            f"Drone({self.label}, zone={self.current_zone}, "
            f"status={self.status.name})"
        )
