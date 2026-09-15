"""Space-time reservation table used for conflict-free multi-drone planning.

Each zone/connection occupancy is tracked per discrete simulation turn.
This lets the pathfinder check, in O(1), whether a given zone or
connection still has free capacity at a given turn before committing a
drone to it — the core mechanism behind the "prioritized planning"
strategy used by :class:`fly_in.core.pathfinder.Pathfinder`.
"""

from __future__ import annotations

from typing import Dict, Tuple


class ReservationTable:
    """Tracks, per simulation turn, how many drones occupy each resource."""

    def __init__(self) -> None:
        self._zone_occupancy: Dict[Tuple[str, int], int] = {}
        self._connection_occupancy: Dict[Tuple[str, int], int] = {}

    def zone_count(self, zone_name: str, turn: int) -> int:
        """Number of drones already resting in ``zone_name`` at ``turn``."""
        return self._zone_occupancy.get((zone_name, turn), 0)

    def connection_count(self, connection_name: str, turn: int) -> int:
        """Number of drones already traversing ``connection_name`` at ``turn``."""
        return self._connection_occupancy.get((connection_name, turn), 0)

    def zone_available(self, zone_name: str, turn: int, capacity: int) -> bool:
        """Whether one more drone could occupy the zone at that turn."""
        return self.zone_count(zone_name, turn) < capacity

    def connection_available(
        self, connection_name: str, turn: int, capacity: int
    ) -> bool:
        """Whether one more drone could traverse the connection at that turn."""
        return self.connection_count(connection_name, turn) < capacity

    def reserve_zone(self, zone_name: str, turn: int) -> None:
        """Book one occupancy slot of ``zone_name`` at ``turn``."""
        key = (zone_name, turn)
        self._zone_occupancy[key] = self._zone_occupancy.get(key, 0) + 1

    def reserve_connection(self, connection_name: str, turn: int) -> None:
        """Book one occupancy slot of ``connection_name`` at ``turn``."""
        key = (connection_name, turn)
        self._connection_occupancy[key] = self._connection_occupancy.get(key, 0) + 1
