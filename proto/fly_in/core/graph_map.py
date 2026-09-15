"""DroneMap: a hand-rolled graph structure (no external graph library).

The whole adjacency logic (nodes, edges, neighbor lookup) is implemented
from scratch on purpose, since the subject forbids the use of any graph
library such as ``networkx`` or ``graphlib``.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

from fly_in.core.connection import Connection
from fly_in.core.zone import Zone


class DroneMap:
    """Owns the zones and connections of the network and their adjacency.

    Attributes:
        nb_drones: Number of drones to route, as declared in the map file.
        zones: Mapping of zone name to :class:`Zone`.
        connections: All connections of the network.
        start_zone_name: Name of the unique start zone.
        end_zone_name: Name of the unique end zone.
    """

    def __init__(self, nb_drones: int) -> None:
        self.nb_drones = nb_drones
        self.zones: Dict[str, Zone] = {}
        self.connections: List[Connection] = []
        self.start_zone_name: str = ""
        self.end_zone_name: str = ""
        self._adjacency: Dict[str, List[Tuple[str, Connection]]] = {}

    def add_zone(self, zone: Zone) -> None:
        """Register a zone and track start/end designation."""
        self.zones[zone.name] = zone
        self._adjacency.setdefault(zone.name, [])
        if zone.is_start:
            self.start_zone_name = zone.name
        if zone.is_end:
            self.end_zone_name = zone.name

    def add_connection(self, connection: Connection) -> None:
        """Register a bidirectional connection and update adjacency lists."""
        self.connections.append(connection)
        self._adjacency.setdefault(connection.zone_a, [])
        self._adjacency.setdefault(connection.zone_b, [])
        self._adjacency[connection.zone_a].append((connection.zone_b, connection))
        self._adjacency[connection.zone_b].append((connection.zone_a, connection))

    def neighbors(self, zone_name: str) -> List[Tuple[Zone, Connection]]:
        """Return the ``(neighbor_zone, connection)`` pairs reachable from a zone."""
        result: List[Tuple[Zone, Connection]] = []
        for neighbor_name, connection in self._adjacency.get(zone_name, []):
            result.append((self.zones[neighbor_name], connection))
        return result

    def get_zone(self, name: str) -> Zone:
        """Fetch a zone by name."""
        return self.zones[name]

    @property
    def start_zone(self) -> Zone:
        """The unique starting zone."""
        return self.zones[self.start_zone_name]

    @property
    def end_zone(self) -> Zone:
        """The unique ending zone."""
        return self.zones[self.end_zone_name]

    def __len__(self) -> int:
        return len(self.zones)

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return (
            f"DroneMap(zones={len(self.zones)}, "
            f"connections={len(self.connections)}, drones={self.nb_drones})"
        )
