*This project has been created as part of the 42 curriculum by srasolov.*

# Fly-in — Drone Routing Simulation

## Description

**Fly-in** is a Python simulation engine that routes a fleet of autonomous
drones from a central base (`start`) to a target location (`end`) through a
network of interconnected zones, while respecting movement constraints, zone
and connection capacities, and minimizing the total number of simulation
turns.

The project is fully object-oriented, does not rely on any external graph
library (no `networkx`, no `graphlib`), and is entirely typesafe (`mypy` /
`flake8` compliant). It includes:

- A hand-written parser for the zone-network map format, with line-accurate
  error reporting.
- A time-aware pathfinding algorithm (A\* over a space-time graph) used both
  to find the shortest route and to diversify routes across multiple drones.
- A turn-by-turn simulation engine that enforces zone/connection capacities,
  handles waiting, and manages multi-turn transits through `restricted`
  zones.
- Two visualization modes: a colored terminal output and a full pygame
  graphical interface with playback controls.
- A benchmark suite comparing performance against the reference turn-count
  targets for every provided map.

## Instructions

### Requirements

- Python 3.11+
- `pygame` and `rich` for runtime use
- `flake8` and `mypy` for development (see `pyproject.toml`)

### Installation

```bash
git clone <repo_url>
cd fly_in
make install
```

`make install` creates a virtual environment (`venv/`) and installs the
runtime and development dependencies declared in `pyproject.toml`.

### Running the simulation

```bash
make run
```

This launches `main.py`, which opens an interactive terminal menu: pick a map
category (`easy`, `medium`, `hard`, `challenger`), then pick a specific map
file. The simulation then runs and prints:

1. A colored, turn-by-turn log of every drone movement in the terminal.
2. A pygame window animating the same simulation on the map.

### Other commands

```bash
make debug      # runs main.py under pdb (uses $MAP, defaults to a hard map)
make lint       # flake8 + mypy (mandatory flags)
make lint-strict  # flake8 + mypy --strict
make benchmark  # runs every provided map against its target turn count
make clean      # removes __pycache__, .mypy_cache, .pytest_cache, *.pyc
```

### Pygame controls

| Key | Action |
| --- | --- |
| `Space` / `P` | Pause / resume |
| `N` / `→` | Next turn |
| `B` / `←` | Previous turn |
| `R` | Restart |
| `+` / `-` | Change playback speed |
| `0` | Reset speed to normal |
| `H` | Show / hide the help panel |
| `Esc` | Quit |

## Resources

- [A\* search algorithm — Wikipedia](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [Dijkstra's algorithm — Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Prioritized planning for multi-agent pathfinding — general concept used for
  drone-to-drone conflict avoidance](https://en.wikipedia.org/wiki/Multi-agent_pathfinding)
- [PEP 257 — Docstring conventions](https://peps.python.org/pep-0257/)
- [pygame documentation](https://www.pygame.org/docs/)
- [Rich documentation](https://rich.readthedocs.io/)
- [mypy documentation](https://mypy.readthedocs.io/)

### AI usage

AI assistance (Claude) was used throughout this project as a **pair-programming
aid**, not as a code generator we copy-pasted blindly — every suggestion was
reviewed, tested, and adapted before being integrated. Specifically, it was
used for:

- Explaining and comparing pathfinding strategies (Dijkstra vs. A\*, and how
  to extend A\* into a space-time graph to reason about multi-drone
  scheduling).
- Debugging assistance: for example, tracing a bug where a drone could move
  twice within the same simulation turn (once completing a `restricted`
  transit, then immediately moving again in the same turn's decision phase),
  which caused a visual glitch in the pygame animation. The fix (tracking
  drones that already moved that turn) was written and verified against the
  actual simulation output before being merged.
- Reviewing Python typing issues (`mypy --strict` compliance) and suggesting
  cleaner patterns (e.g. splitting a single "load image, maybe required"
  helper into two differently-typed helpers so `mypy` could correctly narrow
  `Surface | None` to `Surface`).
- General code review and refactoring suggestions (project structure,
  Makefile rules, `.gitignore`).

No part of the project was accepted without being understood and tested by
both of us — this was a requirement we held ourselves to throughout
development, in line with the project's own guidance on AI usage.

## Algorithm Choices & Implementation Strategy

### Parsing

`Parser` reads the map file line by line, validates it against the format
described in the subject (zone/connection syntax, metadata blocks, duplicate
names, duplicate connections, invalid zone types, non-positive capacities),
and raises a `ParseError` carrying the offending line number and a clear
message on any failure. It never lets a malformed file crash the program with
a raw traceback.

### Data model

- `Zone`: a single node in the network. Knows its own movement cost
  (`normal`/`priority` → 1, `restricted` → 2) and whether it is `blocked`.
- `Connection`: a bidirectional edge between two zones, with an optional
  `max_link_capacity`.
- `DroneMap`: owns all zones and connections and exposes `neighbors(zone)` —
  this is our own graph implementation; no external graph library is used
  anywhere in the project.
- `Drone`: tracks a drone's planned path, current zone, and transit state
  (`in_transit`, `transit_target`, `arrival_turn`) for multi-turn movements.

### Pathfinding — space-time A\*

Rather than searching a purely spatial graph, `SpaceTimePathfinder` searches
over states of the form `(zone, turn)`. This lets the algorithm reason about
**when** a zone or connection will be occupied, not just whether it is
reachable — which is what makes multi-drone conflict avoidance possible in
the first place.

- **Heuristic**: Euclidean distance to the goal zone. It never overestimates
  the true remaining cost (no path can be shorter than a straight line), so
  it is admissible and A\* remains guaranteed optimal while exploring far
  fewer states than plain Dijkstra would.
- **Movement costs**: 1 turn for `normal`/`priority` zones, 2 turns for
  `restricted` zones, and `blocked` zones are excluded from the graph
  entirely rather than being assigned an infinite cost.
- **Restricted zones**: once a drone commits to entering a connection leading
  to a `restricted` zone, it has no "waiting" state mid-connection — it must
  arrive exactly one simulation turn later, matching the subject's
  constraint that a drone "can't wait extra turns on the connection."

### Multi-drone diversification — prioritized planning

Drones are planned one after another, not simultaneously:

1. The first drone searches freely; no slot is reserved yet.
2. Every `(zone, turn)` and `(connection, turn)` it uses is recorded in two
   reservation tables.
3. The next drone's own search treats those slots as unavailable — its A\*
   naturally routes around them, either by waiting or by diverging onto an
   alternative path, whichever is cheaper.
4. This repeats for every drone, producing a natural spread across multiple
   paths whenever the map's topology offers them.

This is a deliberate simplification: each drone's path is computed once,
before the simulation starts, rather than being replanned dynamically while
the simulation runs. This makes it straightforward to reason about (no
mid-simulation deadlocks to prove away) and is sufficient to comfortably meet
every benchmark target provided in the subject — see
[Benchmark Results](#benchmark-results).

### Simulation engine

`SimulationEngine` replays the reserved paths turn by turn, independently
re-checking zone occupancy and connection capacity at each step (since
several drones move concurrently, and a zone freed this turn by one drone can
be taken by another in the same turn). A drone that cannot move because a
zone or connection is full simply waits and retries the following turn.

One subtlety worth calling out: a drone finishing a `restricted` transit and
a drone making a "normal" decision are handled in two separate passes within
the same turn (arrivals first, then new movement decisions). Without care,
a drone that had just arrived could be re-evaluated in the second pass and
move again within the same turn — we track drones that already moved this
turn explicitly to prevent that.

### Complexity

The search space is `O(V · T)` states, where `V` is the number of zones and
`T` is the temporal horizon explored. With the binary heap used for the
priority queue, a single pathfinding call is `O(V · T · log(V · T))` in the
worst case. In practice the heuristic prunes the vast majority of this space
— the benchmark suite, including the 15-drone `ultimate_challenge` map,
completes in a fraction of a second.

## Visual Representation

### Terminal (`TerminalDisplay`)

Prints a colored, turn-by-turn log: each drone ID is assigned a distinct
color, and each destination zone is colored according to the `color`
attribute defined in the map file — so the terminal output visually matches
the same palette used in the pygame view.

### Graphical (`PygameDisplay`)

A full animated view of the simulation:

- Zones are laid out on screen from their `(x, y)` coordinates, drawn as
  colored station icons (with distinct icons for `start` and `end`), and
  connected by lines matching the map's connection graph.
- Drones are rendered as sprites that **smoothly interpolate** between their
  position at turn *t* and turn *t+1*, so a drone completing a two-turn
  `restricted` transit visibly travels across the map rather than
  teleporting.
- A HUD shows the current turn, run/pause status, and playback speed; a
  bottom panel echoes the exact move log for the turn currently on screen.
- Full playback control (pause, step forward/backward, restart, adjustable
  speed) lets a reviewer freeze the simulation on any turn and inspect it —
  which is what let us catch and fix the double-move bug described above in
  the first place: it was visible as a drone's animation cutting in a
  straight line between two zones that aren't actually connected on the map.

## Example Input & Output

Input map (`maps/easy/02_simple_fork.txt`):

```text
# Easy Level 2: Simple fork with two paths
nb_drones: 4

start_hub: start 0 0 [color=green]
hub: junction 1 0 [color=yellow max_drones=2]
hub: path_a 2 1 [color=blue zone=restricted]
hub: path_b 2 -1 [color=blue ]
end_hub: goal 3 0 [color=red]

connection: start-junction [max_link_capacity=2]
connection: junction-path_a
connection: junction-path_b
connection: path_a-goal
connection: path_b-goal
```

Program output (terminal, abbreviated):

```text
Loaded 5 zones, 4 drones
Start: start -> End: goal

Turn 1: D1-junction D2-junction D3-wait D4-wait
Turn 2: D1-path_b D2-junction-path_a D3-junction D4-junction
Turn 3: D2-path_a D1-goal D3-path_b D4-wait
Turn 4: D2-goal D3-goal D4-path_b
Turn 5: D4-goal

Total turns: 5
```

D2's route illustrates the `restricted`-zone rule directly: at turn 2 it
announces entering the `junction-path_a` connection, and only arrives at
`path_a` at turn 3 — one full turn later, with no way to stop in between —
before continuing on to `goal`. D1, D3 and D4 are automatically routed
through `path_b` instead, an example of the diversification described above.

## Benchmark Results

Run with `make benchmark`. All provided maps meet their target turn count:

| Map | Turns | Target | Result |
| --- | ---: | ---: | --- |
| easy/01_linear_path | 4 | ≤ 6 | OK |
| easy/02_simple_fork | 5 | ≤ 6 | OK |
| easy/03_basic_capacity | 4 | ≤ 6 | OK |
| medium/01_dead_end_trap | 8 | ≤ 12 | OK |
| medium/02_circular_loop | 15 | ≤ 15 | OK |
| medium/03_priority_puzzle | 7 | ≤ 12 | OK |
| hard/01_maze_nightmare | 13 | ≤ 20 | OK |
| hard/02_capacity_hell | 16 | ≤ 25 | OK |
| hard/03_ultimate_challenge | 26 | ≤ 30 | OK |

## Project Structure

```text
fly_in/
├── main.py                  # Entry point: map menu, parsing, simulation, display
├── benchmark.py              # Runs every map against its target turn count
├── pyproject.toml
├── Makefile
├── generator/
│   ├── models.py              # Zone, Connection, DroneMap
│   ├── parser.py               # Map file parser and ParseError
│   ├── pathfinding.py            # SpaceTimePathfinder (space-time A*)
│   ├── drone.py                # Drone state and transit tracking
│   ├── simulation.py             # SimulationEngine (turn-by-turn logic)
│   ├── terminal_display.py         # Colored terminal output
│   ├── display.py               # Pygame graphical display
│   └── readfile.py              # Interactive map-selection menu
├── assets/                  # Background and sprite images for pygame
└── maps/
    ├── easy/
    ├── medium/
    ├── hard/
    └── challenger/
```
