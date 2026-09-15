"""Zone model: a node of the drone network graph."""

from __future__ import annotations

from enum import Enum
from typing import Optional


class ZoneType(Enum):
    """The four supported zone types and their movement cost in turns."""

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"

    @property
    def is_traversable(self) -> bool:
        """Whether a drone is allowed to enter a zone of this type."""
        return self is not ZoneType.BLOCKED

    @property
    def movement_cost(self) -> int:
        """Number of simulation turns required to move *into* this zone type.

        Raises:
            ValueError: If called on a BLOCKED zone type, which has no cost
                since it can never be entered.
        """
        costs = {
            ZoneType.NORMAL: 1,
            ZoneType.PRIORITY: 1,
            ZoneType.RESTRICTED: 2,
        }
        if self not in costs:
            raise ValueError(f"Zone type {self} is not traversable.")
        return costs[self]

    @property
    def is_priority(self) -> bool:
        """Whether pathfinding should prefer this zone type, all else equal."""
        return self is ZoneType.PRIORITY


class Zone:
    """A single zone (node) of the drone network.

    Attributes:
        name: Unique identifier of the zone.
        x: X coordinate (used only for display purposes).
        y: Y coordinate (used only for display purposes).
        zone_type: The :class:`ZoneType` of this zone.
        color: Optional color tag used for visual representation.
        max_drones: Maximum number of drones that may occupy this zone at
            the same simulation turn.
        is_start: Whether this zone is the unique starting hub.
        is_end: Whether this zone is the unique ending hub.
    """

    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        zone_type: ZoneType = ZoneType.NORMAL,
        color: Optional[str] = None,
        max_drones: int = 1,
        is_start: bool = False,
        is_end: bool = False,
    ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.color = color
        self.max_drones = max_drones
        self.is_start = is_start
        self.is_end = is_end

    @property
    def has_unlimited_capacity(self) -> bool:
        """Start and end zones are exempt from occupancy limits."""
        return self.is_start or self.is_end

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return (
            f"Zone(name={self.name!r}, type={self.zone_type.value}, "
            f"max_drones={self.max_drones}, start={self.is_start}, "
            f"end={self.is_end})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Zone):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
