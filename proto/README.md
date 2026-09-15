*This project has been created as part of the 42 curriculum by <your_login>.*

# Fly-in — Multi-Drone Routing Simulator

## Description

**Fly-in** routes a fleet of autonomous drones through a network of zones,
from a unique start hub to a unique end hub, in the fewest possible
simulation turns. The network topology, zone types (`normal`,
`priority`, `restricted`, `blocked`), zone/connection capacities and the
number of drones are all described in a small custom text format (see
`maps/` for examples, including the exact map given in the subject).

The simulator:

- Parses and strictly validates the map file (custom hand-written parser,
  no external parsing library).
- Computes a conflict-free, minimal-turn schedule for every drone using a
  custom graph and pathfinding implementation (no `networkx`, no
  `graphlib`, no third-party graph library of any kind).
- Simulates the network turn by turn, respecting zone occupancy limits,
  connection capacities, and the special two-turn "committed" traversal
  of `restricted` zones.
- Prints a colored, human-readable overview of the network and of the
  turn-by-turn simulation log directly in the terminal.

The whole project is written in an object-oriented style and is fully
type-checked (`mypy --strict`) and `flake8`-clean.

## Instructions

### Requirements

- Python 3.10+
- No third-party runtime dependency is required to *run* the simulator
  (the colored output only uses raw ANSI escape codes). `flake8`, `mypy`
  and `pytest` are only needed for development/linting/testing.

### Setup

```bash
make install     # installs flake8, mypy and pytest (dev tools only)
```

### Running the simulator

```bash
make run                              # runs the bundled example map
make run MAP=maps/hard_maze.txt       # runs a specific map
python3 -m fly_in.main maps/easy_linear.txt          # equivalent, direct call
python3 -m fly_in.main maps/easy_linear.txt --quiet  # raw log only, no colors
python3 -m fly_in.main maps/easy_linear.txt --pygame # animated graphical view
```

### Other Makefile targets

| Target        | Description                                              |
|---------------|-----------------------------------------------------------|
| `install`     | Install development dependencies.                         |
| `run`         | Run the simulator on `$(MAP)` (defaults to the subject example). |
| `debug`       | Run the simulator under Python's built-in debugger (`pdb`). |
| `test`        | Run the (non-graded) `pytest` unit test suite.             |
| `lint`        | Run `flake8` and `mypy` with the flags required by the subject. |
| `lint-strict` | Run `flake8` and `mypy --strict`.                          |
| `clean`       | Remove `__pycache__`, `.mypy_cache` and `.pytest_cache`.   |

### Project layout

```
fly_in/
  core/
    exceptions.py   -> custom error types (parsing / unreachable path)
    zone.py         -> Zone + ZoneType (movement cost, capacity, ...)
    connection.py   -> Connection (bidirectional edge)
    drone.py        -> Drone (lifecycle: waiting / in transit / delivered)
    graph_map.py    -> DroneMap: hand-rolled graph structure & adjacency
    parser.py       -> MapParser: strict text-format parser
    reservation.py  -> ReservationTable: space-time occupancy bookkeeping
    pathfinder.py   -> Pathfinder: time-expanded Dijkstra search
    simulator.py    -> Simulator: orchestrates all drones, builds the log
    visualizer.py   -> ANSI-colored terminal and Pygame rendering
  main.py           -> CLI entry point
maps/               -> sample map files (easy / medium / hard)
tests/              -> pytest unit tests (not graded, for our own confidence)
```

## Algorithm Choices & Implementation Strategy

### Modeling movement as a time-expanded graph

Every zone type has a movement *cost* expressed in simulation turns
(`normal`/`priority` = 1, `restricted` = 2, `blocked` = never
traversable). Rather than reasoning turn-by-turn imperatively, each
drone's route is computed as a shortest path over an implicit
**time-expanded graph**: a search state is a pair `(zone, turn)`
meaning *"the drone rests in `zone` right after `turn` has elapsed"*.
From a state, two actions are explored:

- **Wait** one turn in place (if the zone still has free capacity next
  turn).
- **Move** to a neighboring zone through a connection, advancing the
  turn counter by the destination zone's movement cost, provided the
  connection *and* the destination zone both have free capacity for
  every turn of the traversal.

A classic **Dijkstra search** (all edge weights are positive: 1 or 2)
finds the earliest turn at which the end zone can be reached. Since
`priority` zones should be *preferred*, not just allowed, ties between
equally-fast routes are broken using a secondary key that rewards paths
crossing more priority zones — implemented as a lexicographic
`(turn, -priority_zone_count)` ordering in the search's priority queue.

### Coordinating multiple drones: prioritized planning

Drones may move simultaneously and must never violate zone or
connection capacities. Instead of jointly optimizing all drones at
once (an NP-hard combinatorial problem for anything but toy inputs),
this project uses **prioritized planning**: drones are scheduled one
after another, in ID order, and each drone's Dijkstra search is run
against a single shared `ReservationTable` that already contains every
previously scheduled drone's route. A later drone will naturally wait
(via the "wait" action) whenever a zone or connection it needs is
already booked, which is exactly how deadlocks and collisions are
avoided.

This trade-off is deliberate:

- **Pro**: simple, deterministic, easy to prove correct (each committed
  path is, by construction, conflict-free with everything scheduled
  before it), and fast enough for the required scale (tested with 25
  drones, sub-30ms end-to-end).
- **Con**: it is not globally optimal — an earlier-scheduled drone can
  occasionally force a later one into a longer detour that a
  globally-aware planner might have avoided. For the map sizes and
  drone counts targeted by this subject, this did not prevent meeting
  or beating every benchmark turn count provided.

### Restricted zones: the "commit or don't move" rule

A move into a `restricted` zone costs 2 turns and, per the subject,
*cannot* be interrupted or delayed mid-flight. This is naturally
enforced by only ever exploring **whole** moves in the search (a
2-turn move is a single atomic edge of the time-expanded graph, never
two separate 1-turn edges), so a drone can never be "stuck" waiting on
a connection.

### Complexity

Let `Z` be the number of zones, `E` the number of connections and `H`
the search horizon (an adaptive upper bound on turns, doubling from a
base of 300 up to 5000 if needed — in practice a single map never
requires growing past the base horizon).

- Each drone's search visits at most `O(Z * H)` states, each with
  `O(deg)` neighbors, for a total of `O(Z * H * E)` per drone with a
  binary heap, i.e. `O(Z * H * E * log(Z * H))`.
- For `N` drones this gives a total complexity of roughly
  `O(N * Z * H * E * log(Z * H))`.
- **Memory**: the `ReservationTable` only stores `(resource, turn)` keys
  that are actually used (a Python dict), so memory scales with the
  number of *occupied* slots, not with `Z * H` — negligible for the
  map sizes involved (a few hundred to a few thousand entries even for
  the 25-drone stress test).
- **No caching/memoization across drones** is performed on purpose:
  each drone's optimal path genuinely depends on the reservations left
  by previously scheduled drones, so a cached "static" shortest path
  would be incorrect more often than not.

In practice, on the provided example map (5 drones, 7 zones) the whole
simulation runs in well under a millisecond; the 25-drone, 10-hub
stress test used during development completes in about 10
milliseconds.

## Visual Representation

The `Visualizer` (see `fly_in/core/visualizer.py`) provides two
complementary colored terminal views, built entirely on raw ANSI escape
codes (no third-party dependency):

1. **Network overview**: every zone is listed with its coordinates,
   type, capacity, and a color derived either from its explicit
   `color=` tag (mapped to the closest ANSI color) or, if unspecified,
   from its zone type (`restricted` "warns" in yellow, `blocked` is
   dimmed gray, `priority` is green, etc.), making bottlenecks and
   danger zones immediately visible before the simulation even starts.
2. **Turn-by-turn simulation log**: each turn is printed on its own
   line, prefixed with its turn number, and every drone's move is
   colored with a distinct, stable per-drone color (recycled from an
   8-color palette) so that a single drone's journey can be visually
   followed across turns at a glance — genuinely useful once several
   drones are in flight simultaneously.
3. A final **summary** block reports the total number of turns, drones
   delivered, total path cost, and average turns per drone, to make it
   easy to compare a run against the subject's performance benchmarks.

Pass `--quiet` to the CLI to get only the raw, uncolored turn-by-turn
log (`D<id>-<zone_or_connection>` lines), matching exactly the output
format required by the subject — useful for automated grading or
piping into another tool.

## Resources

- [Dijkstra's algorithm — Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Time-expanded graphs for multi-agent path finding](https://en.wikipedia.org/wiki/Multi-agent_pathfinding)
- [Python `heapq` documentation](https://docs.python.org/3/library/heapq.html)
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)
- [mypy documentation](https://mypy.readthedocs.io/)
- [flake8 documentation](https://flake8.pycqa.org/)

### AI usage disclosure

An AI assistant (Claude, Anthropic) was used during this project for:

- Drafting the initial object-oriented architecture (module split between
  `Zone`, `Connection`, `DroneMap`, `Pathfinder`, `ReservationTable`,
  `Simulator`, `Visualizer`) based on the constraints of the subject.
- Writing the regex-based parser and its validation error paths.
- Designing and implementing the time-expanded Dijkstra search and the
  prioritized-planning scheduling loop.
- Writing the ANSI-based terminal visualizer.
- Drafting this README and the accompanying unit tests.

Every generated piece of code was read, run against the provided
example map and the custom maps in `maps/`, checked with `flake8` and
`mypy --strict`, and cross-checked against the subject's rules
(zone/connection capacity semantics, the restricted-zone commit rule,
the exact output format) before being kept. As recommended in the
subject's AI Instructions chapter, no part of this project should be
treated as understood or defensible until you can personally explain
and, if needed, modify every function above — take the time to trace
through `Pathfinder._search` by hand on a small map before your
evaluation.
