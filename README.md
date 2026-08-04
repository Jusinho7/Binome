*This project was created as part of the 42 training program by srasolov and maeandri.*

# A-Maze-ing

## Description

A-Maze-ing is a Python maze generator and viewer. Given a small config
file, it builds a rectangular maze (optionally "perfect", i.e. with
exactly one path between the entry and the exit), embeds a visible "42"
made of fully-closed cells somewhere in the grid, writes the result to a
plain-text file using a compact hexadecimal wall encoding, and lets you
explore it interactively in the terminal with colored ASCII art.

The maze-generation logic itself lives in a small, standalone, reusable
library (`mazegen`) that has no dependency on the CLI, the config format,
or the display code, so it can be dropped into another project as-is.

## Instructions

### Requirements

- Python 3.10+
- `pip install -r requirements-dev.txt` (flake8, mypy, build) for
  development tooling.

### Run

```bash
make run                     # uses config.txt by default
# or directly:
python3 a_maze_ing.py config.txt
```

The program:
1. parses `config.txt`,
2. generates the maze,
3. writes it to the configured `OUTPUT_FILE`,
4. opens an interactive ASCII viewer in the terminal.

Interactive viewer controls:

```
1. Re-generate a new maze
2. Show/hide path from entry to exit
3. Rotate maze colors
4. Quit
```

### Other Makefile targets

```bash
make install       # install dev dependencies
make debug         # run under pdb
make lint          # flake8 + mypy (subject-mandated options)
make lint-strict   # flake8 --strict-ish + mypy --strict
make package        # rebuild the mazegen-*.whl at the repo root
make clean          # remove caches/build artifacts
```

### Configuration file format

One `KEY=VALUE` pair per line; lines starting with `#` are comments.

| Key           | Description                              | Example              |
|---------------|-------------------------------------------|-----------------------|
| `WIDTH`       | Maze width in cells                       | `WIDTH=20`             |
| `HEIGHT`      | Maze height in cells                      | `HEIGHT=15`            |
| `ENTRY`       | Entry coordinates `x,y`                   | `ENTRY=0,0`            |
| `EXIT`        | Exit coordinates `x,y`                    | `EXIT=19,14`           |
| `OUTPUT_FILE` | Path of the generated maze file           | `OUTPUT_FILE=maze.txt` |
| `PERFECT`     | *(optional, default `True`)* `True`/`False` — exactly one path or not | `PERFECT=True` |
| `SEED`        | *(optional)* RNG seed, for reproducibility | `SEED=42`             |

`ENTREE`/`SORTIE`/`FICHIER_SORTIE`/`HAUTEUR`/`GRAINE` are also accepted as
aliases of `ENTRY`/`EXIT`/`OUTPUT_FILE`/`HEIGHT`/`SEED`.

### Output file format

- One line per maze row; one hexadecimal digit per cell, encoding which of
  its walls are closed: bit 0 = North, bit 1 = East, bit 2 = South,
  bit 3 = West (1 = closed, 0 = open).
- A blank line.
- Entry coordinates (`x,y`).
- Exit coordinates (`x,y`).
- The shortest entry → exit path as a string of `N`/`E`/`S`/`W` letters.

All lines end with `\n`.

### Reusable `mazegen` module

Building the wheel:

```bash
python3 -m build --wheel -o dist
cp dist/mazegen-*.whl .
```

A pre-built `mazegen-1.0.0-py3-none-any.whl` is already provided at the
repository root; install it with:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

Usage:

```python
from mazegen import MazeGenerator

generator = MazeGenerator(
    width=20, height=15, seed=42, perfect=True,
    entry=(0, 0), exit=(19, 14),
)
generator.generate()

walls = generator.get_walls()        # walls[y][x] bitmask, see encoding above
solution = generator.shortest_path()  # e.g. "SSEENNW..."
```

See `mazegen/README.md` for the full API reference (also duplicated
above in short form, as required).

## Maze generation algorithm

**Iterative recursive-backtracker (randomized DFS)** carved over every
non-pattern cell, starting from the entry, using a seeded
`random.Random` instance for reproducibility.

Why this algorithm:
- It naturally produces a **spanning tree**, so a "perfect" maze
  (`PERFECT=True`) falls out for free — no extra cycle-detection pass is
  needed.
- Because a spanning tree has no cycles, it can never contain a fully
  open 2×2 (or larger) block, which directly satisfies the "no open area
  wider than 2 cells" requirement without additional bookkeeping.
- It is simple, fast, and easy to reason about/debug compared to
  Kruskal's or Prim's algorithms, while producing mazes with a similar
  visual "long winding corridor" character.

When `PERFECT=False`, a bounded number of extra walls are randomly opened
on top of the spanning tree to introduce loops; each candidate is
verified (by scanning the surrounding 3×3 windows) to never create an
open area of 3×3 cells or larger before being accepted.

The "42" pattern is a small bitmap of fully-closed cells centered in the
grid, reserved *before* carving so the backtracker treats it as outside
the walkable graph — exactly the "isolated cells" exception called out
in the subject. If the maze is too small to fit the pattern, generation
still proceeds and a warning is printed to the console.

## What's reusable, and how

Everything under `mazegen/` (the `MazeGenerator` class, wall bit
encoding, pathfinding, and the "42" pattern) is fully decoupled from:
- the config file format (`config.py`),
- the on-disk output format (`output_writer.py`),
- and the terminal UI (`display/ascii_display.py`).

Any of those three layers can be swapped out (e.g. a graphical MLX
renderer, a JSON config format, a different output encoding) without
touching `mazegen` at all. That's also why `mazegen` ships as its own
installable wheel, independent of the rest of the repository.

## Team & project management

- **srasolov**: ASCII display (interactive terminal rendering,
  menu) and the backtracker generation algorithm.
- **maeandri**: config parsing/validation and the BFS
  pathfinding algorithm.
- **Shared**: overall project structure and keeping the codebase
  modular (decoupling `mazegen` from the config/output/display
  layers).
- **Tools** used: Python 3, flake8, mypy, `build` (PEP 517 wheel
  builder).

## Resources

- Backtracking: [Mastering Backtracking: From LeetCode to Real-World Applications](https://medium.com/@hanxuyang0826/mastering-backtracking-from-leetcode-to-real-world-applications-4c9150de20da)
- BFS: [Breadth-First Search (BFS)](https://medium.com/@prajun_t/breadth-first-search-bfs-db7ffb384da7)
- Bit manipulation: [Bit Operation: Solving Algorithm Problem in Python](https://medium.com/@pcheng5/bit-operation-solving-algorithm-problem-in-python-42a375efd3eb)
- pip: [Pip in Python: what it is and how to install packages](https://www.luisllamas.es/python-como-usar-pip/)
- Poetry: [POETRY](https://python-poetry.org/docs/basic-usage/)
- Makefiles: [MAKEFILE](https://earthly.dev/blog/python-makefile/)
- Packaging: [PACKAGE](https://blog.stephane-robert.info/docs/developper/programmation/python/modules/)

## AI Usage

- Explanation and understanding of key concepts (bit manipulation,
  backtracking, BFS).
- Generation of the wall-encoding logic and the "42" pattern
  placement.
- Debugging (mypy/flake8 errors, rendering bugs, config parsing
  edge cases).
