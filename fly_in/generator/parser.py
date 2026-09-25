"""Parse a drone map definition file and populate a DroneMap object."""

import re
from typing import Optional
from .models import Connection, DroneMap, Zone


class ParseError(Exception):
    """Represent an error encountered while parsing a map file."""

    def __init__(self, line_number: int, message: str) -> None:
        """Initialize a parse error with its source line number.

        Args:
            line_number: Number of the line where the error occurred.
            message: Description of the parsing error.
        """
        super().__init__(f"Line {line_number}: {message}")
        self.line_number = line_number


VALID_ZONE_TYPES = {"normal", "blocked", "restricted", "priority"}
COLORS = [
    "green",
    "red",
    "yellow",
    "blue",
    "gray",
    "purple",
    "orange",
    "pink",
    "brown",
    "black",
    "white",
    "cyan",
    "magenta",
    "lime",
    "teal",
    "navy",
    "maroon",
    "olive",
    "silver",
    "gold",
    "beige",
    "lavender",
    "coral",
    "salmon",
    "khaki",
    "plum",
    "orchid",
    "turquoise",
    "indigo",
    "violet",
    "peach",
    "mint",
    "cream",
    "tan",
    "chocolate",
    "charcoal",
    "burgundy",
    "mustard",
    "rust",
    "sienna",
    "amber",
    "cerulean",
    "periwinkle",
    "fuchsia",
    "darkred",
    "crimson",
    "rainbow",
]
RED = "\033[31m"
RESET = "\033[0m"


class Parser:
    """Parse a drone map definition file."""

    def __init__(self, filepath: str) -> None:
        """Initialize a parser for the specified map file.

        Args:
            filepath: Path to the map definition file.
        """
        self.filepath = filepath

    def parse(self) -> DroneMap:
        """Parse the map file and return a populated drone map.

        Returns:
            A drone map containing the parsed zones and connections.

        Raises:
            ParseError: If the map file contains invalid or incomplete data.
        """
        drone_map = DroneMap()
        nb_drones: Optional[int] = None

        with open(self.filepath, "r", encoding="utf-8") as handle:
            lines = handle.readlines()

        first_content_line = True
        for i, raw_line in enumerate(lines, start=1):
            line = raw_line.strip()

            if not line or line.startswith("#"):
                continue

            nb_drones_match = re.fullmatch(r"nb_drones\s*:\s*(.*)", line)
            start_hub_match = re.fullmatch(r"start_hub\s*:\s*(.*)", line)
            end_hub_match = re.fullmatch(r"end_hub\s*:\s*(.*)", line)
            hub_match = re.fullmatch(r"hub\s*:\s*(.*)", line)
            Connection_match = re.fullmatch(r"connection\s*:\s*(.*)", line)

            if first_content_line and nb_drones_match is None:
                raise ParseError(
                    i,
                    f"{RED}'nb_drones' must be the first declaration{RESET}",
                )
            first_content_line = False

            if line.startswith("nb_drones"):
                if nb_drones_match is None:
                    raise ParseError(
                        i,
                        f"{RED}invalid 'nb_drones' declaration{RESET}",
                    )
                if nb_drones is not None:
                    raise ParseError(
                        i,
                        f"{RED}duplicate 'nb_drones' declaration{RESET}",
                    )
                nb_drones = self._parse_nb_drones(
                    f"nb_drones: {nb_drones_match.group(1)}", i
                )
            elif line.startswith("start_hub"):
                if start_hub_match is None:
                    raise ParseError(
                        i,
                        f"{RED}invalid 'start_hub' declaration{RESET}",
                    )
                self._parse_zone(line, i, drone_map, is_start=True)
            elif line.startswith("end_hub"):
                if end_hub_match is None:
                    raise ParseError(
                        i,
                        f"{RED}invalid 'end_hub' declaration{RESET}",
                    )
                self._parse_zone(line, i, drone_map, is_end=True)
            elif line.startswith("hub"):
                if hub_match is None:
                    raise ParseError(
                        i,
                        f"{RED}invalid 'hub' declaration{RESET}",
                    )
                self._parse_zone(line, i, drone_map)
            elif line.startswith("connection"):
                if Connection_match is None:
                    raise ParseError(
                        i,
                        f"{RED}invalid 'connection' declaration{RESET}",
                    )
                self._parse_connection(line, i, drone_map)
            else:
                raise ParseError(i, f"{RED}unrecognized line: '{line}'{RESET}")

        if nb_drones is None:
            raise ParseError(
                1,
                f"{RED}missing 'nb_drones' declaration{RESET}",
            )
        if drone_map.start is None:
            raise ParseError(0, f"{RED}missing 'start_hub' zone{RESET}")
        if drone_map.end is None:
            raise ParseError(0, f"{RED}missing 'end_hub' zone{RESET}")
        if (
            drone_map.start.x == drone_map.end.x
            and drone_map.start.y == drone_map.end.y
        ):
            raise ParseError(
                0,
                f"{RED}start_hub and end_hub cannot share the same "
                f"coordinates{RESET}",
            )

        drone_map.nb_drones = nb_drones
        return drone_map

    def _parse_nb_drones(self, line: str, line_no: int) -> int:
        """Parse and validate the number of drones.

        Args:
            line: Source line containing the drone count.
            line_no: Number of the source line.

        Returns:
            The validated number of drones.

        Raises:
            ParseError: If the value is missing, invalid, or out of range.
        """
        try:
            value = line.split(":", 1)[1].strip()
            if "_" in value:
                raise ParseError(
                    line_no,
                    f"{RED}invalid nb_drones value: {value}{RESET}"
                )
            nb = int(value)
        except (IndexError, ValueError):
            raise ParseError(
                line_no,
                f"{RED}invalid nb_drones value{RESET}",
            )
        if nb <= 0:
            raise ParseError(
                line_no,
                f"{RED}nb_drones must be a positive integer{RESET}",
            )
        if nb > 100:
            raise ParseError(
                line_no,
                f"{RED}nb_drones must not exceed 100{RESET}",
            )
        return nb

    def _parse_zone(
        self,
        line: str,
        line_no: int,
        drone_map: DroneMap,
        is_start: bool = False,
        is_end: bool = False,
    ) -> None:
        """Parse a zone declaration and add it to the drone map.

        Args:
            line: Source line containing the zone declaration.
            line_no: Number of the source line.
            drone_map: Map receiving the parsed zone.
            is_start: Whether the zone is the simulation start hub.
            is_end: Whether the zone is the simulation end hub.

        Raises:
            ParseError: If the zone declaration or metadata is invalid.
        """
        _, rest = line.split(":", 1)
        rest = rest.strip()

        metadata_str = ""
        if "[" in rest:
            rest, metadata_part = rest.split("[", 1)
            if not metadata_part.strip().endswith("]"):
                raise ParseError(
                    line_no,
                    f"{RED}malformed metadata block, missing ']'{RESET}",
                )
            metadata_str = metadata_part.strip()[:-1]
            duplicate_check = metadata_str.split()
            pile: list[str] = []
            for token in duplicate_check:
                if "=" not in token:
                    raise ParseError(
                        line_no,
                        f"{RED}invalid metadata token '{token}'{RESET}",
                    )
                key, value = token.split("=", 1)
                if key not in ["zone", "color", "max_drones"]:
                    raise ParseError(
                        line_no,
                        f"{RED}invalid metadata key '{key}'{RESET}",
                    )
                pile.append(key)
                if value == "":
                    raise ParseError(
                        line_no,
                        f"{RED}metadata key '{key}' has empty value{RESET}",
                    )
                if key == "color" and value not in COLORS:
                    raise ParseError(
                        line_no,
                        f"{RED}invalid color value '{value}'{RESET}",
                    )
            if len(pile) != len(set(pile)):
                raise ParseError(
                    line_no,
                    f"{RED}duplicate metadata keys in zone definition{RESET}",
                )

        parts = rest.strip().split()
        if len(parts) != 3:
            raise ParseError(
                line_no,
                f"{RED}expected '<name> <x> <y>', got '{rest.strip()}'"
                f"{RESET}",
            )

        name, x_str, y_str = parts

        if "-" in name or " " in name:
            raise ParseError(
                line_no,
                f"{RED}invalid zone name '{name}' "
                f"(no dashes/spaces allowed){RESET}",
            )
        if name in drone_map.zones:
            raise ParseError(
                line_no,
                f"{RED}duplicate zone name '{name}'{RESET}",
            )

        try:
            if "_" in y_str:
                raise ParseError(
                    line_no,
                    f"{RED}zone coordinate invalid: {y_str}{RESET}"
                )

            if "_" in x_str:
                raise ParseError(
                    line_no,
                    f"{RED}zone coordinate invalid: {x_str}{RESET}"
                )

            x, y = int(x_str), int(y_str)
        except ValueError:
            raise ParseError(
                line_no,
                f"{RED}zone coordinates must be integers{RESET}",
            )

        for existing_zone in drone_map.zones.values():
            if existing_zone.x == x and existing_zone.y == y:
                raise ParseError(
                    line_no,
                    f"{RED}coordinates ({x}, {y}) are already used by "
                    f"zone '{existing_zone.name}'{RESET}",
                )

        metadata = self._parse_metadata(metadata_str, line_no)

        zone_type = metadata.get("zone", "normal")
        if zone_type not in VALID_ZONE_TYPES:
            raise ParseError(
                line_no,
                f"{RED}invalid zone type '{zone_type}'{RESET}",
            )

        color = metadata.get("color")

        max_drones_str = metadata.get("max_drones")
        if is_start or is_end:
            max_drones: Optional[int] = None
        elif max_drones_str is not None:
            max_drones = self._parse_positive_int(
                max_drones_str,
                line_no,
                "max_drones",
            )
        else:
            max_drones = 1

        zone = Zone(
            name=name,
            x=x,
            y=y,
            zone_type=zone_type,
            color=color,
            max_drones=max_drones,
        )
        drone_map.add_zone(zone)

        if is_start:
            drone_map.start = zone
        if is_end:
            drone_map.end = zone

    def _parse_connection(
        self,
        line: str,
        line_no: int,
        drone_map: DroneMap,
    ) -> None:
        """Parse a connection declaration and add it to the drone map.

        Args:
            line: Source line containing the connection declaration.
            line_no: Number of the source line.
            drone_map: Map receiving the parsed connection.

        Raises:
            ParseError: If the connection syntax, zones, or metadata is
            invalid.
        """
        _, rest = line.split(":", 1)
        rest = rest.strip()

        metadata_str = ""
        if "[" in rest:
            rest, metadata_part = rest.split("[", 1)
            if not metadata_part.strip().endswith("]"):
                raise ParseError(
                    line_no,
                    f"{RED}malformed metadata block, missing ']'{RESET}",
                )
            metadata_str = metadata_part.strip()[:-1]

        names = rest.strip().split("-")
        if len(names) != 2:
            raise ParseError(
                line_no,
                f"{RED}invalid connection syntax: '{rest.strip()}'{RESET}",
            )

        name_a, name_b = names[0].strip(), names[1].strip()

        if name_a == name_b:
            raise ParseError(
                line_no,
                f"{RED}a connection cannot point to the same zone: "
                f"'{name_a}-{name_b}'{RESET}",
            )

        if name_a not in drone_map.zones or name_b not in drone_map.zones:
            raise ParseError(
                line_no,
                f"{RED}connection references undefined zone(s): "
                f"{name_a}-{name_b}{RESET}",
            )

        zone_a, zone_b = drone_map.zones[name_a], drone_map.zones[name_b]

        for existing in drone_map.connections:
            if {existing.zone_a.name, existing.zone_b.name} == {
                name_a,
                name_b,
            }:
                raise ParseError(
                    line_no,
                    f"{RED}duplicate connection '{name_a}-{name_b}'{RESET}",
                )

        metadata = self._parse_metadata(metadata_str, line_no)
        capacity_str = metadata.get("max_link_capacity")
        capacity = (
            self._parse_positive_int(
                capacity_str,
                line_no,
                "max_link_capacity",
            )
            if capacity_str is not None
            else 1
        )

        drone_map.add_connection(
            Connection(zone_a, zone_b, max_link_capacity=capacity)
        )

    def _parse_metadata(
        self,
        metadata_str: str,
        line_no: int,
    ) -> dict[str, str]:
        """Parse a metadata block into key-value pairs.

        Args:
            metadata_str: Metadata text without the surrounding brackets.
            line_no: Number of the source line.

        Returns:
            A dictionary containing metadata keys and values.

        Raises:
            ParseError: If a metadata token does not contain ``=``.
        """
        metadata: dict[str, str] = {}
        if not metadata_str:
            return metadata

        for token in metadata_str.split():
            if "=" not in token:
                raise ParseError(
                    line_no,
                    f"{RED}invalid metadata token '{token}'{RESET}",
                )
            key, value = token.split("=", 1)
            metadata[key] = value
        return metadata

    def _parse_positive_int(
        self,
        value: str,
        line_no: int,
        field_name: str,
    ) -> int:
        """Parse and validate a positive integer field.

        Args:
            value: String representation of the integer.
            line_no: Number of the source line.
            field_name: Name of the field being validated.

        Returns:
            The validated positive integer.

        Raises:
            ParseError: If the value is not a positive integer.
        """
        try:
            if "_" in value:
                raise ParseError(
                    line_no,
                    f"{RED}value is invalid: {value}{RESET}"
                )
            n = int(value)
        except ValueError:
            raise ParseError(
                line_no,
                f"{RED}'{field_name}' must be an integer{RESET}",
            )
        if n <= 0:
            raise ParseError(
                line_no,
                f"{RED}'{field_name}' must be a positive integer{RESET}",
            )
        return n
