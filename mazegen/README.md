# mazegen

A small, dependency-free, reusable maze generation library, extracted from
the *A-Maze-ing* project so it can be imported into other projects.

## Install

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

## Quick start

```python
from mazegen import MazeGenerator

# Instantiate the generator with custom parameters (size, seed, entry/exit,
# and whether the maze must be "perfect" — exactly one path between any
# two cells).
generator = MazeGenerator(
    width=20,
    height=15,
    seed=42,          # reproducible generation
    perfect=True,
    entry=(0, 0),
    exit=(19, 14),
)

# Build the maze.
generator.generate()

# Access the generated structure: walls[y][x] is a bitmask
# (bit0=North, bit1=East, bit2=South, bit3=West -> 1 means closed).
walls = generator.get_walls()

# Access at least one solution, as a string of N/E/S/W moves.
solution = generator.shortest_path()
```

## API

- `MazeGenerator(width, height, seed=None, perfect=True, entry=(0, 0),
  exit=(0, 0), embed_pattern=True)` — create a generator.
- `generate()` — build the maze in place.
- `get_walls()` — return the wall grid (`list[list[int]]`, `walls[y][x]`).
- `get_pattern_cells()` — return the set of cells forming the embedded
  "42" pattern (fully-closed, isolated cells), if it fit in the maze.
- `shortest_path(start=None, end=None)` — BFS shortest path between two
  cells (defaults to entry/exit) as a string of `N`/`E`/`S`/`W` letters.

Note: the structure returned by `get_walls()` is the library's own
in-memory representation; it is not necessarily the same layout as the
on-disk output file format used by the `a_maze_ing.py` CLI.
