"""Unit tests for the map parser."""

from __future__ import annotations

import pytest

from fly_in.core.exceptions import MapParsingError
from fly_in.core.parser import MapParser
from fly_in.core.zone import ZoneType


def test_parses_subject_example() -> None:
    parser = MapParser()
    drone_map = parser.parse_file("maps/example_subject.txt")

    assert drone_map.nb_drones == 5
    assert drone_map.start_zone_name == "hub"
    assert drone_map.end_zone_name == "goal"
    assert drone_map.get_zone("roof1").zone_type is ZoneType.RESTRICTED
    assert drone_map.get_zone("corridorA").max_drones == 2
    assert len(drone_map.connections) == 6


def test_rejects_dash_in_zone_name() -> None:
    lines = [
        "nb_drones: 1\n",
        "start_hub: base 0 0\n",
        "end_hub: goal 1 0\n",
        "hub: bad-name 0 1\n",
        "connection: base-goal\n",
    ]
    with pytest.raises(MapParsingError):
        MapParser().parse_lines(lines)


def test_rejects_invalid_zone_type() -> None:
    lines = [
        "nb_drones: 1\n",
        "start_hub: base 0 0\n",
        "end_hub: goal 1 0\n",
        "hub: x 0 1 [zone=unknown]\n",
        "connection: base-x\n",
        "connection: x-goal\n",
    ]
    with pytest.raises(MapParsingError):
        MapParser().parse_lines(lines)


def test_rejects_duplicate_connection() -> None:
    lines = [
        "nb_drones: 1\n",
        "start_hub: base 0 0\n",
        "end_hub: goal 1 0\n",
        "hub: x 0 1\n",
        "connection: base-x\n",
        "connection: x-base\n",
    ]
    with pytest.raises(MapParsingError):
        MapParser().parse_lines(lines)


def test_rejects_missing_end_hub() -> None:
    lines = [
        "nb_drones: 1\n",
        "start_hub: base 0 0\n",
        "hub: x 0 1\n",
        "connection: base-x\n",
    ]
    with pytest.raises(MapParsingError):
        MapParser().parse_lines(lines)


def test_ignores_comments_and_blank_lines() -> None:
    lines = [
        "# a comment\n",
        "nb_drones: 1\n",
        "\n",
        "start_hub: base 0 0\n",
        "end_hub: goal 1 0\n",
        "# another comment\n",
        "connection: base-goal\n",
    ]
    drone_map = MapParser().parse_lines(lines)
    assert len(drone_map.zones) == 2


def test_rejects_negative_capacity() -> None:
    lines = [
        "nb_drones: 1\n",
        "start_hub: base 0 0\n",
        "end_hub: goal 1 0\n",
        "hub: x 0 1 [max_drones=-1]\n",
        "connection: base-x\n",
        "connection: x-goal\n",
    ]
    with pytest.raises(MapParsingError):
        MapParser().parse_lines(lines)
