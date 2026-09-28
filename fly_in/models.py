"""Core map types for the Fly-in simulation."""

from typing import Optional


class Zone:
    """Represent a single hub or zone on the map."""

    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        zone_type: str = "normal",
        color: Optional[str] = None,
        max_drones: Optional[int] = 1,
    ) -> None:
        """Initialize a zone with its coordinates and behavior."""
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.color = color
        self.max_drones = max_drones

    def movement_cost(self) -> int:
        """Return the traversal cost for this zone."""
        if self.zone_type == "restricted":
            return 2
        return 1

    def is_blocked(self) -> bool:
        """Return whether this zone blocks movement."""
        return self.zone_type == "blocked"


class Connection:
    """Represent a bidirectional link between two zones."""

    def __init__(
        self,
        zone_a: Zone,
        zone_b: Zone,
        max_link_capacity: int = 1,
    ) -> None:
        """Initialize a connection with its endpoints and capacity."""
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity

    def other(self, zone: Zone) -> Zone:
        """Return the opposite endpoint of this connection."""
        return self.zone_b if zone is self.zone_a else self.zone_a


class DroneMap:
    """Store the full map topology and all entities involved in routing."""

    def __init__(self) -> None:
        """Initialize an empty map."""
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.start: Optional[Zone] = None
        self.end: Optional[Zone] = None
        self.nb_drones: int = 0

    def add_zone(self, zone: Zone) -> None:
        """Add a new zone to the map."""
        self.zones[zone.name] = zone

    def add_connection(self, connection: Connection) -> None:
        """Add a new connection to the map."""
        self.connections.append(connection)

    def neighbors(self, zone: Zone) -> list[Connection]:
        """Return all connections incident to the provided zone."""
        return [
            c
            for c in self.connections
            if c.zone_a is zone or c.zone_b is zone
        ]
