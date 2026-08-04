"""Generate mazes and provide access to their structure and paths."""

import random
from typing import Optional
from .pattern42 import PATTERN_42, PATTERN_HEIGHT, PATTERN_WIDTH
from .exceptions import MazeGenerationError
from .pathfinding import shortest_path as _bfs_shortest_path
from .carving import carve_spanning_tree, add_loops
from .directions import FULLY_CLOSED

__all__ = ["MazeGenerator", "MazeGenerationError"]


class MazeGenerator:
    """Generate and manage a rectangular maze."""

    def __init__(
        self,
        width: int,
        height: int,
        seed: Optional[int] = None,
        perfect: bool = True,
        entry: tuple[int, int] = (0, 0),
        exit: tuple[int, int] = (0, 0),
        embed_pattern: bool = True,
    ) -> None:
        """Initialize a maze generator."""
        if width < 1 or height < 1:
            raise MazeGenerationError("width and height must be >= 1")
        if width > 62 or height > 62:
            raise MazeGenerationError("width and height must be <= 62")
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self.entry = entry
        self.exit = exit
        self.embed_pattern = embed_pattern
        self._rng = random.Random(seed)
        self._walls: list[list[int]] = [
            [FULLY_CLOSED for _ in range(width)] for _ in range(height)
        ]
        self._pattern_cells: set[tuple[int, int]] = set()
        self._generated = False
        self.pattern_warning: Optional[str] = None

    def generate(self) -> None:
        """Generate the maze in place."""
        self._validate_entry_exit()
        self._place_pattern()
        self._carve_spanning_tree()
        if not self.perfect:
            self._add_loops()
        self._generated = True

    def get_walls(self) -> list[list[int]]:
        """Return a copy of the maze wall grid."""
        self._ensure_generated()
        return [row[:] for row in self._walls]

    def get_pattern_cells(self) -> set[tuple[int, int]]:
        """Return the cells occupied by the 42 pattern."""
        return set(self._pattern_cells)

    def shortest_path(
        self,
        start: Optional[tuple[int, int]] = None,
        end: Optional[tuple[int, int]] = None,
    ) -> str:
        """Return the shortest path between two cells."""
        self._ensure_generated()
        start = start or self.entry
        end = end or self.exit
        return _bfs_shortest_path(self._walls, start, end)

    def _ensure_generated(self) -> None:
        """Ensure that the maze has been generated."""
        if not self._generated:
            raise MazeGenerationError("generate() must be called first")

    def _in_bounds(self, x: int, y: int) -> bool:
        """Return whether the given coordinates are inside the maze."""
        return 0 <= x < self.width and 0 <= y < self.height

    def _validate_entry_exit(self) -> None:
        """Validate the entry and exit coordinates."""
        for name, (x, y) in (("entry", self.entry), ("exit", self.exit)):
            if not self._in_bounds(x, y):
                raise MazeGenerationError(f"{name} {(x, y)} is out of bounds")
        if self.entry == self.exit:
            raise MazeGenerationError("entry and exit must be different")

    def _place_pattern(self) -> None:
        """Reserve cells for the 42 pattern when possible."""
        if not self.embed_pattern:
            return
        margin = 1
        needed_w = PATTERN_WIDTH + margin * 2
        needed_h = PATTERN_HEIGHT + margin * 2
        if self.width < needed_w or self.height < needed_h:
            self.pattern_warning = (
                "Maze too small to embed the '42' pattern "
                f"(needs at least {needed_w + 2}x{needed_h})."
            )
            print(f"[warning] {self.pattern_warning}")
            return

        ox = (self.width - PATTERN_WIDTH) // 2
        oy = (self.height - PATTERN_HEIGHT) // 2
        candidate: set[tuple[int, int]] = set()
        for row_idx, row in enumerate(PATTERN_42):
            for col_idx, ch in enumerate(row):
                if ch == "1":
                    candidate.add((ox + col_idx, oy + row_idx))

        if self.entry in candidate or self.exit in candidate:
            self.pattern_warning = (
                "Entry/exit collide with the '42' pattern; pattern skipped."
            )
            print(f"[warning] {self.pattern_warning}")
            return

        self._pattern_cells = candidate

    def _carve_spanning_tree(self) -> None:
        """Delegate spanning-tree carving to the carving module."""
        carve_spanning_tree(
            self._walls,
            self.width,
            self.height,
            self.entry,
            self._pattern_cells,
            self._rng,
        )

    def _add_loops(self, extra_ratio: float = 0.12) -> None:
        """Add extra loops to the maze."""
        add_loops(
            self._walls,
            self.width,
            self.height,
            self._pattern_cells,
            self._rng,
            extra_ratio=extra_ratio,
        )
