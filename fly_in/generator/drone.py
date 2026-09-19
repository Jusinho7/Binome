from typing import Optional

from .models import Zone


class Drone:
    def __init__(self, drone_id: int, start_zone: Zone) -> None:
        self.id = drone_id
        self.current_zone = start_zone
        self.path: list[Zone] = []
        self.path_index = 0
        self.delivered = False
        self.in_transit = False
        self.transit_target: Optional[Zone] = None
        self.arrival_turn: Optional[int] = None

    def set_path(self, path: list[Zone]) -> None:
        self.path = path
        self.path_index = 0

    def next_zone(self) -> Optional[Zone]:
        if self.path_index + 1 < len(self.path):
            return self.path[self.path_index + 1]
        return None

    def start_transit(self, target: Zone, arrival_turn: int) -> None:
        self.in_transit = True
        self.transit_target = target
        self.arrival_turn = arrival_turn

    def complete_transit(self) -> None:
        target = self.transit_target
        if target is None:
            raise ValueError("Cannot complete a transit without a target zone")
        self.current_zone = target
        self.path_index += 1
        self.in_transit = False
        self.transit_target = None
        self.arrival_turn = None

    def advance_direct(self, target: Zone) -> None:
        self.current_zone = target
        self.path_index += 1
