from typing import Optional
from models import Zone, Connection, DroneMap


class ParseError(Exception):
    def __init__(self, line_number: int, message: str) -> None:
        super().__init__(f"Line {line_number}: {message}")
        self.line_number = line_number


VALID_ZONE_TYPES = {"normal", "blocked", "restricted", "priority"}


class Parser:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def parse(self) -> DroneMap:
        drone_map = DroneMap()
        nb_drones: Optional[int] = None

        with open(self.filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for i, raw_line in enumerate(lines, start=1):
            line = raw_line.strip()

            if not line or line.startswith("#"):
                continue

            if line.startswith("nb_drones:"):
                nb_drones = self._parse_nb_drones(line, i)
            elif line.startswith("start_hub:"):
                self._parse_zone(line, i, drone_map, is_start=True)
            elif line.startswith("end_hub:"):
                self._parse_zone(line, i, drone_map, is_end=True)
            elif line.startswith("hub:"):
                self._parse_zone(line, i, drone_map)
            elif line.startswith("connection:"):
                self._parse_connection(line, i, drone_map)
            else:
                raise ParseError(i, f"unrecognized line: '{line}'")

        if nb_drones is None:
            raise ParseError(1, "missing 'nb_drones' declaration")
        if drone_map.start is None:
            raise ParseError(0, "missing 'start_hub' zone")
        if drone_map.end is None:
            raise ParseError(0, "missing 'end_hub' zone")

        drone_map.nb_drones = nb_drones
        return drone_map

    def _parse_nb_drones(self, line: str, line_no: int) -> int:
        try:
            value = line.split(":", 1)[1].strip()
            nb = int(value)
        except (IndexError, ValueError):
            raise ParseError(line_no, "invalid nb_drones value")
        if nb <= 0:
            raise ParseError(line_no, "nb_drones must be a positive integer")
        return nb

    def _parse_zone(
        self,
        line: str,
        line_no: int,
        drone_map: DroneMap,
        is_start: bool = False,
        is_end: bool = False,
    ) -> None:
        prefix, rest = line.split(":", 1)
        rest = rest.strip()

        metadata_str = ""
        if "[" in rest:
            rest, metadata_part = rest.split("[", 1)
            if not metadata_part.strip().endswith("]"):
                raise ParseError(line_no, "malformed metadata block, missing ']'")
            metadata_str = metadata_part.strip()[:-1]

        parts = rest.strip().split()
        if len(parts) != 3:
            raise ParseError(line_no, f"expected '<name> <x> <y>', got '{rest.strip()}'")

        name, x_str, y_str = parts

        if "-" in name or " " in name:
            raise ParseError(line_no, f"invalid zone name '{name}' (no dashes/spaces allowed)")
        if name in drone_map.zones:
            raise ParseError(line_no, f"duplicate zone name '{name}'")

        try:
            x, y = int(x_str), int(y_str)
        except ValueError:
            raise ParseError(line_no, "zone coordinates must be integers")

        metadata = self._parse_metadata(metadata_str, line_no)

        zone_type = metadata.get("zone", "normal")
        if zone_type not in VALID_ZONE_TYPES:
            raise ParseError(line_no, f"invalid zone type '{zone_type}'")

        color = metadata.get("color")

        max_drones_str = metadata.get("max_drones")
        if is_start or is_end:
            max_drones = None
        elif max_drones_str is not None:
            max_drones = self._parse_positive_int(max_drones_str, line_no, "max_drones")
        else:
            max_drones = 1

        zone = Zone(name=name, x=x, y=y, zone_type=zone_type, color=color, max_drones=max_drones)
        drone_map.add_zone(zone)

        if is_start:
            drone_map.start = zone
        if is_end:
            drone_map.end = zone

    def _parse_connection(self, line: str, line_no: int, drone_map: DroneMap) -> None:
        _, rest = line.split(":", 1)
        rest = rest.strip()

        metadata_str = ""
        if "[" in rest:
            rest, metadata_part = rest.split("[", 1)
            if not metadata_part.strip().endswith("]"):
                raise ParseError(line_no, "malformed metadata block, missing ']'")
            metadata_str = metadata_part.strip()[:-1]

        names = rest.strip().split("-")
        if len(names) != 2:
            raise ParseError(line_no, f"invalid connection syntax: '{rest.strip()}'")

        name_a, name_b = names[0].strip(), names[1].strip()

        if name_a not in drone_map.zones or name_b not in drone_map.zones:
            raise ParseError(line_no, f"connection references undefined zone(s): {name_a}-{name_b}")

        zone_a, zone_b = drone_map.zones[name_a], drone_map.zones[name_b]

        for existing in drone_map.connections:
            if {existing.zone_a.name, existing.zone_b.name} == {name_a, name_b}:
                raise ParseError(line_no, f"duplicate connection '{name_a}-{name_b}'")

        metadata = self._parse_metadata(metadata_str, line_no)
        capacity_str = metadata.get("max_link_capacity")
        capacity = (
            self._parse_positive_int(capacity_str, line_no, "max_link_capacity")
            if capacity_str is not None
            else 1
        )

        drone_map.add_connection(Connection(zone_a, zone_b, max_link_capacity=capacity))

    def _parse_metadata(self, metadata_str: str, line_no: int) -> dict[str, str]:
        metadata: dict[str, str] = {}
        if not metadata_str:
            return metadata

        for token in metadata_str.split():
            if "=" not in token:
                raise ParseError(line_no, f"invalid metadata token '{token}'")
            key, value = token.split("=", 1)
            metadata[key] = value
        return metadata

    def _parse_positive_int(self, value: str, line_no: int, field_name: str) -> int:
        try:
            n = int(value)
        except ValueError:
            raise ParseError(line_no, f"'{field_name}' must be an integer")
        if n <= 0:
            raise ParseError(line_no, f"'{field_name}' must be a positive integer")
        return n