"""Unit tests for the mazegen package (run with pytest)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest  # noqa: E402

from mazegen import MazeGenerationError, MazeGenerator  # noqa: E402


def test_reproducible_with_seed() -> None:
    g1 = MazeGenerator(15, 10, seed=1, entry=(0, 0), exit=(14, 9))
    g2 = MazeGenerator(15, 10, seed=1, entry=(0, 0), exit=(14, 9))
    g1.generate()
    g2.generate()
    assert g1.get_walls() == g2.get_walls()


def test_perfect_maze_is_a_spanning_tree() -> None:
    width, height = 15, 10
    gen = MazeGenerator(
        width, height, seed=2, perfect=True, entry=(0, 0), exit=(14, 9)
    )
    gen.generate()
    walls = gen.get_walls()
    pattern = gen.get_pattern_cells()
    free_cells = width * height - len(pattern)

    open_edges = 0
    for y in range(height):
        for x in range(width):
            if (x, y) in pattern:
                continue
            east_open = not (walls[y][x] & 0b0010)
            if x + 1 < width and (x + 1, y) not in pattern and east_open:
                open_edges += 1
            south_open = not (walls[y][x] & 0b0100)
            if y + 1 < height and (x, y + 1) not in pattern and south_open:
                open_edges += 1
    assert open_edges == free_cells - 1


def test_wall_consistency_between_neighbors() -> None:
    gen = MazeGenerator(12, 8, seed=3, entry=(0, 0), exit=(11, 7))
    gen.generate()
    walls = gen.get_walls()
    for y in range(8):
        for x in range(12):
            if x + 1 < 12:
                east = bool(walls[y][x] & 0b0010)
                west_neighbor = bool(walls[y][x + 1] & 0b1000)
                assert east == west_neighbor
            if y + 1 < 8:
                south = bool(walls[y][x] & 0b0100)
                north_neighbor = bool(walls[y + 1][x] & 0b0001)
                assert south == north_neighbor


def test_boundary_walls_are_closed() -> None:
    width, height = 10, 6
    gen = MazeGenerator(width, height, seed=4, entry=(0, 0), exit=(9, 5))
    gen.generate()
    walls = gen.get_walls()
    for x in range(width):
        assert walls[0][x] & 0b0001
        assert walls[height - 1][x] & 0b0100
    for y in range(height):
        assert walls[y][0] & 0b1000
        assert walls[y][width - 1] & 0b0010


def test_no_3x3_open_area() -> None:
    width, height = 20, 15
    gen = MazeGenerator(
        width, height, seed=5, perfect=False, entry=(0, 0), exit=(19, 14)
    )
    gen.generate()
    walls = gen.get_walls()

    def open_east(x: int, y: int) -> bool:
        return not (walls[y][x] & 0b0010)

    def open_south(x: int, y: int) -> bool:
        return not (walls[y][x] & 0b0100)

    for oy in range(height - 2):
        for ox in range(width - 2):
            fully_open = True
            for row in range(3):
                for col in range(2):
                    if not open_east(ox + col, oy + row):
                        fully_open = False
            for col in range(3):
                for row in range(2):
                    if not open_south(ox + col, oy + row):
                        fully_open = False
            assert not fully_open


def test_shortest_path_matches_direction_letters() -> None:
    gen = MazeGenerator(10, 10, seed=6, entry=(0, 0), exit=(9, 9))
    gen.generate()
    path = gen.shortest_path()
    deltas = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
    x, y = gen.entry
    for letter in path:
        dx, dy = deltas[letter]
        x, y = x + dx, y + dy
    assert (x, y) == gen.exit


def test_invalid_entry_raises() -> None:
    gen = MazeGenerator(5, 5, entry=(0, 0), exit=(0, 0))
    with pytest.raises(MazeGenerationError):
        gen.generate()


def test_out_of_bounds_entry_raises() -> None:
    gen = MazeGenerator(5, 5, entry=(10, 10), exit=(1, 1))
    with pytest.raises(MazeGenerationError):
        gen.generate()


def test_pattern_embedded_when_maze_large_enough() -> None:
    gen = MazeGenerator(20, 15, seed=7, entry=(0, 0), exit=(19, 14))
    gen.generate()
    assert len(gen.get_pattern_cells()) > 0
    assert gen.pattern_warning is None


def test_pattern_skipped_when_maze_too_small() -> None:
    gen = MazeGenerator(6, 6, seed=8, entry=(0, 0), exit=(5, 5))
    gen.generate()
    assert len(gen.get_pattern_cells()) == 0
    assert gen.pattern_warning is not None
