"""Drone state and path-tracking logic."""

from typing import Optional
from .models import Zone


class Drone:
    """Represent a drone and its movement state across the map."""

    def __init__(self, drone_id: int, start_zone: Zone) -> None:
        """Initialize a drone with its identifier and starting zone."""
        self.id = drone_id
        self.current_zone = start_zone
        self.path: list[Zone] = []
        self.path_index = 0
        self.delivered = False
        self.in_transit = False
        self.transit_target: Optional[Zone] = None
        self.arrival_turn: Optional[int] = None

    def set_path(self, path: list[Zone]) -> None:
        """Store a new planned path for the drone."""
        self.path = path
        self.path_index = 0

    def next_zone(self) -> Optional[Zone]:
        """Return the next zone on the current path, if any."""
        if self.path_index + 1 < len(self.path):
            return self.path[self.path_index + 1]
        return None

    def start_transit(self, target: Zone, arrival_turn: int) -> None:
        """Begin a timed transit to a target zone."""
        self.in_transit = True
        self.transit_target = target
        self.arrival_turn = arrival_turn

    def complete_transit(self) -> None:
        """Finish a transit and advance the drone to its destination."""
        target = self.transit_target
        if target is None:
            raise ValueError("Cannot complete a transit without a target zone")
        self.current_zone = target
        self.path_index += 1
        self.in_transit = False
        self.transit_target = None
        self.arrival_turn = None

    def advance_direct(self, target: Zone) -> None:
        """Advance the drone directly to the next zone."""
        self.current_zone = target
        self.path_index += 1
