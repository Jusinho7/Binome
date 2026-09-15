"""Unit tests for the pathfinder and simulator."""

from __future__ import annotations

from fly_in.core.parser import MapParser
from fly_in.core.simulator import Simulator


def _run(path: str) -> tuple[int, int]:
    drone_map = MapParser().parse_file(path)
    result = Simulator(drone_map).run()
    return result.total_turns, result.drones_delivered


def test_linear_map_matches_expected_turns() -> None:
    total_turns, delivered = _run("maps/easy_linear.txt")
    assert delivered == 2
    assert total_turns <= 6


def test_fork_map_uses_both_paths() -> None:
    total_turns, delivered = _run("maps/easy_fork.txt")
    assert delivered == 3
    assert total_turns <= 6


def test_capacity_map_respects_benchmark() -> None:
    total_turns, delivered = _run("maps/easy_capacity.txt")
    assert delivered == 4
    assert total_turns <= 8


def test_subject_example_all_drones_delivered() -> None:
    total_turns, delivered = _run("maps/example_subject.txt")
    assert delivered == 5
    assert total_turns > 0


def test_no_zone_ever_exceeds_capacity() -> None:
    drone_map = MapParser().parse_file("maps/hard_maze.txt")
    result = Simulator(drone_map).run()

    occupancy: dict[tuple[str, int], int] = {}
    for turn_log in result.turns:
        for action in turn_log.actions:
            _, destination = action.split("-", 1)
            if destination in drone_map.zones:
                key = (destination, turn_log.turn)
                occupancy[key] = occupancy.get(key, 0) + 1

    for (zone_name, _turn), count in occupancy.items():
        zone = drone_map.get_zone(zone_name)
        if zone.has_unlimited_capacity:
            continue
        assert count <= zone.max_drones


def test_no_connection_ever_exceeds_capacity() -> None:
    drone_map = MapParser().parse_file("maps/medium_loop.txt")
    result = Simulator(drone_map).run()

    by_connection = {c.name: c for c in drone_map.connections}
    occupancy: dict[tuple[str, int], int] = {}
    for turn_log in result.turns:
        for action in turn_log.actions:
            _, destination = action.split("-", 1)
            if destination in by_connection:
                key = (destination, turn_log.turn)
                occupancy[key] = occupancy.get(key, 0) + 1

    for (conn_name, _turn), count in occupancy.items():
        assert count <= by_connection[conn_name].max_link_capacity
