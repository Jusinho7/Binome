"""Parser turning a map description file into a :class:`DroneMap`.

The custom text format is described in the project subject. This module
implements a strict, hand-written parser (no external parsing library)
that validates every rule listed in the "Parser Constraints" section:
uniqueness of names, valid zone types, positive capacities, no duplicate
connections, etc. Any violation raises a :class:`MapParsingError` that
points at the offending line.
"""

from __future__ import annotations

import re
from typing import Dict, Optional

from fly_in.core.connection import Connection
from fly_in.core.exceptions import MapParsingError
from fly_in.core.graph_map import DroneMap
from fly_in.core.zone import Zone, ZoneType

_ZONE_NAME_PATTERN = re.compile(r"^[^\s-]+$")
_METADATA_PATTERN = re.compile(r"\[(.*)\]")
_ZONE_LINE_PATTERN = re.compile(
    r"^(?P<kind>start_hub|end_hub|hub):\s*"
    r"(?P<name>\S+)\s+(?P<x>\S+)\s+(?P<y>\S+)\s*(?P<metadata>\[.*\])?\s*$"
)
_CONNECTION_LINE_PATTERN = re.compile(
    r"^connection:\s*(?P<zone1>[^\s-]+)-(?P<zone2>[^\s-]+)\s*(?P<metadata>\[.*\])?\s*$"
)
_NB_DRONES_PATTERN = re.compile(r"^nb_drones:\s*(?P<value>\S+)\s*$")

_VALID_ZONE_TYPES = {zt.value for zt in ZoneType}


class MapParser:
    """Parses a drone network map file into a :class:`DroneMap` instance."""

    def parse_file(self, path: str) -> DroneMap:
        """Read and parse a map file from disk.

        Args:
            path: Filesystem path to the map description file.

        Returns:
            A fully populated, validated :class:`DroneMap`.

        Raises:
            MapParsingError: If the file content violates the format.
        """
        with open(path, "r", encoding="utf-8") as handle:
            lines = handle.readlines()
        return self.parse_lines(lines)

    def parse_lines(self, lines: list[str]) -> DroneMap:
        """Parse the raw lines of a map file.

        Args:
            lines: The raw lines of the file, in order.

        Returns:
            A fully populated, validated :class:`DroneMap`.

        Raises:
            MapParsingError: If the content violates the format.
        """
        nb_drones: Optional[int] = None
        drone_map: Optional[DroneMap] = None
        seen_connections: Dict[frozenset[str], int] = {}
        start_seen = False
        end_seen = False

        for line_number, raw_line in enumerate(lines, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            if nb_drones is None:
                nb_drones = self._parse_nb_drones(line_number, raw_line)
                drone_map = DroneMap(nb_drones)
                continue

            assert drone_map is not None  # for mypy: set right after nb_drones

            if line.startswith(("start_hub:", "end_hub:", "hub:")):
                zone = self._parse_zone_line(line_number, raw_line)
                if zone.name in drone_map.zones:
                    raise MapParsingError(
                        line_number, raw_line, f"duplicate zone name {zone.name!r}"
                    )
                if zone.is_start:
                    if start_seen:
                        raise MapParsingError(
                            line_number, raw_line, "a start_hub is already defined"
                        )
                    start_seen = True
                if zone.is_end:
                    if end_seen:
                        raise MapParsingError(
                            line_number, raw_line, "an end_hub is already defined"
                        )
                    end_seen = True
                drone_map.add_zone(zone)
                continue

            if line.startswith("connection:"):
                connection = self._parse_connection_line(line_number, raw_line)
                for endpoint in (connection.zone_a, connection.zone_b):
                    if endpoint not in drone_map.zones:
                        raise MapParsingError(
                            line_number,
                            raw_line,
                            f"connection references undefined zone {endpoint!r}",
                        )
                key = frozenset((connection.zone_a, connection.zone_b))
                if key in seen_connections:
                    raise MapParsingError(
                        line_number,
                        raw_line,
                        f"duplicate connection between {connection.zone_a!r} "
                        f"and {connection.zone_b!r}",
                    )
                seen_connections[key] = line_number
                drone_map.add_connection(connection)
                continue

            raise MapParsingError(line_number, raw_line, "unrecognized line format")

        if nb_drones is None or drone_map is None:
            raise MapParsingError(0, "", "missing 'nb_drones:' declaration")
        if not start_seen:
            raise MapParsingError(0, "", "no start_hub zone defined")
        if not end_seen:
            raise MapParsingError(0, "", "no end_hub zone defined")

        return drone_map

    def _parse_nb_drones(self, line_number: int, raw_line: str) -> int:
        match = _NB_DRONES_PATTERN.match(raw_line.strip())
        if not match:
            raise MapParsingError(
                line_number, raw_line, "expected first line 'nb_drones: <int>'"
            )
        value = match.group("value")
        if not value.isdigit() or int(value) <= 0:
            raise MapParsingError(
                line_number, raw_line, "nb_drones must be a positive integer"
            )
        return int(value)

    def _parse_zone_line(self, line_number: int, raw_line: str) -> Zone:
        match = _ZONE_LINE_PATTERN.match(raw_line.strip())
        if not match:
            raise MapParsingError(
                line_number,
                raw_line,
                "expected '<start_hub|end_hub|hub>: <name> <x> <y> [metadata]'",
            )
        name = match.group("name")
        if not _ZONE_NAME_PATTERN.match(name):
            raise MapParsingError(
                line_number, raw_line, f"invalid zone name {name!r} (no dashes/spaces)"
            )

        x = self._parse_int(line_number, raw_line, match.group("x"), "x coordinate")
        y = self._parse_int(line_number, raw_line, match.group("y"), "y coordinate")

        metadata = self._parse_metadata(line_number, raw_line, match.group("metadata"))

        zone_type_str = metadata.pop("zone", ZoneType.NORMAL.value)
        if zone_type_str not in _VALID_ZONE_TYPES:
            raise MapParsingError(
                line_number, raw_line, f"invalid zone type {zone_type_str!r}"
            )
        zone_type = ZoneType(zone_type_str)

        color = metadata.pop("color", None)

        max_drones_str = metadata.pop("max_drones", "1")
        max_drones = self._parse_positive_int(
            line_number, raw_line, max_drones_str, "max_drones"
        )

        if metadata:
            unknown = ", ".join(sorted(metadata))
            raise MapParsingError(
                line_number, raw_line, f"unknown zone metadata key(s): {unknown}"
            )

        kind = match.group("kind")
        return Zone(
            name=name,
            x=x,
            y=y,
            zone_type=zone_type,
            color=color,
            max_drones=max_drones,
            is_start=(kind == "start_hub"),
            is_end=(kind == "end_hub"),
        )

    def _parse_connection_line(self, line_number: int, raw_line: str) -> Connection:
        match = _CONNECTION_LINE_PATTERN.match(raw_line.strip())
        if not match:
            raise MapParsingError(
                line_number,
                raw_line,
                "expected 'connection: <zone1>-<zone2> [metadata]'",
            )
        zone1, zone2 = match.group("zone1"), match.group("zone2")
        if zone1 == zone2:
            raise MapParsingError(
                line_number, raw_line, "a connection cannot link a zone to itself"
            )

        metadata = self._parse_metadata(line_number, raw_line, match.group("metadata"))
        capacity_str = metadata.pop("max_link_capacity", "1")
        capacity = self._parse_positive_int(
            line_number, raw_line, capacity_str, "max_link_capacity"
        )

        if metadata:
            unknown = ", ".join(sorted(metadata))
            raise MapParsingError(
                line_number, raw_line, f"unknown connection metadata key(s): {unknown}"
            )

        return Connection(zone1, zone2, max_link_capacity=capacity)

    def _parse_metadata(
        self, line_number: int, raw_line: str, metadata_block: Optional[str]
    ) -> Dict[str, str]:
        if not metadata_block:
            return {}
        inner_match = _METADATA_PATTERN.match(metadata_block.strip())
        if not inner_match:
            raise MapParsingError(line_number, raw_line, "malformed metadata block")
        inner = inner_match.group(1).strip()
        if not inner:
            return {}

        result: Dict[str, str] = {}
        for token in inner.split():
            if "=" not in token:
                raise MapParsingError(
                    line_number, raw_line, f"malformed metadata tag {token!r}"
                )
            key, _, value = token.partition("=")
            if not key or not value:
                raise MapParsingError(
                    line_number, raw_line, f"malformed metadata tag {token!r}"
                )
            if key in result:
                raise MapParsingError(
                    line_number, raw_line, f"duplicate metadata key {key!r}"
                )
            result[key] = value
        return result

    def _parse_int(
        self, line_number: int, raw_line: str, value: str, label: str
    ) -> int:
        try:
            return int(value)
        except ValueError as exc:
            raise MapParsingError(
                line_number, raw_line, f"{label} must be an integer, got {value!r}"
            ) from exc

    def _parse_positive_int(
        self, line_number: int, raw_line: str, value: str, label: str
    ) -> int:
        if not value.isdigit() or int(value) <= 0:
            raise MapParsingError(
                line_number,
                raw_line,
                f"{label} must be a positive integer, got {value!r}",
            )
        return int(value)
