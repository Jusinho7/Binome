*This project has been created as part of the 42 curriculum by srasolov.*

# Fly-in

## Description

Fly-in is a drone routing and scheduling simulation inspired by dynamic transport problems and constrained pathfinding. The program reads a map description, computes routes for several drones, enforces zone and connection capacities, and simulates time-based movement until every drone reaches its destination.

The project is centered on a graph-based model of hubs and connections. Each zone can have a specific type (normal, restricted, blocked, priority), while each connection may have a limited capacity. The objective is not only to find a path from the start hub to the end hub, but to do so while respecting simultaneous constraints and avoiding deadlocks or bottlenecks.

In practical terms, the simulation reproduces a real-world coordination challenge: multiple drones must move through shared infrastructure without colliding in bottlenecks or overloading restricted segments. The project includes a terminal display, a visual Pygame animation, and map selection utilities to test different scenarios.

## Instructions

### Requirements

This project relies on the following Python packages:

- Python 3.11+
- pygame
- rich

They are listed in `requirements.txt`.

### Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Execution

From the project root:

```bash
python3 main.py
```

The program first offers a map selection interface, then loads the chosen scenario, runs the simulation, prints the turn-by-turn activity in the terminal, and finally opens the animated visualization window.

### Useful commands

```bash
make run
make benchmark
make lint-strict
```

- `make run` launches the simulation.
- `make benchmark` runs the benchmark suite against the provided maps.
- `make lint-strict` performs strict type checking and lint validation.

## Algorithm and implementation strategy

### Core model

The project models the environment as a graph:

- `Zone`: a hub with coordinates, a type, and a capacity limit
- `Connection`: an edge between two zones with a maximum transmission capacity
- `DroneMap`: the full map containing all zones, connections, start, and end hubs

This structure is defined in the `generator/models.py` module.

### Parsing and validation

The parser reads custom map files describing:

- the number of drones
- start and end hubs
- intermediary hubs
- connections between hubs
- optional metadata such as color and capacity

This validation is handled in `generator/parser.py`. It detects malformed declarations and rejects illegal configurations before the simulation begins.

### Pathfinding strategy

The main pathfinding logic is built around a time-aware variant of A* implemented in `generator/pathfinding.py`.

The algorithm does not only consider spatial distance; it also tracks time reservations for:

- zones already occupied at a given turn
- connections already used during a given turn

This is essential because restricted zones and shared links can be traversed only under capacity constraints. The algorithm keeps a state as `(zone_name, turn)` and searches for a valid route that respects time and occupancy constraints.

### Simulation engine

The `SimulationEngine` in `generator/simulation.py` orchestrates drone movement turn by turn:

1. all drones are initialized at the start zone
2. each drone computes a route respecting the current reservations
3. the simulation advances one turn at a time
4. drones either move directly, wait, or start a delayed transit through restricted areas
5. all occupied zones and connection usage are updated after each turn

This allows the system to handle concurrency safely, avoid deadlocks, and preserve realistic timing behavior.

### Handling restricted movement and capacity

Restricted zones incur a cost of 2 turns instead of 1, and are treated as time-sensitive transit points. Before moving into such a zone, the simulation checks whether the destination still has available capacity when the drone would arrive. This is the key to preserving correctness in more advanced maps.

The same logic is applied for connection usage. If a link is already saturated at a specific turn, the drone must wait or select another route.

### Data flow

The application flow is:

1. select a map
2. parse and validate the map
3. instantiate the simulation engine
4. compute the drone routes
5. display the terminal summary
6. run the visual animation in Pygame

This orchestration is centralized in `main.py` and the object model exposed by the generator package.

## Visual representation and user experience

The visual display is implemented in `generator/display.py` and provides a strong user experience for understanding the simulation.

### Features

- map rendering using a background image and spatial layout scaling
- color-coded hubs for start, end, and intermediate zones
- connection lines between zones
- animated drone icons moving on the graph
- HUD showing the current turn, simulation speed, and controls
- help panel with keyboard shortcuts

### Controls

- `Space`: pause/resume
- `R`: restart
- `+ / -`: increase or decrease speed
- `N` / `B`: next/previous turn
- `H`: toggle help panel
- `Escape`: quit

This visual layer makes the algorithm easier to understand, especially for debugging route conflicts, evaluating queueing behavior, and observing how drones interact when capacities are tight.

## Example input and expected output

### Example map

File: `maps/easy/01_linear_path.txt`

```text
# Easy Level 1: Simple linear path
nb_drones: 2

start_hub: start 0 0 [color=green]
hub: waypoint1 1 0 [color=blue]
hub: waypoint2 2 0 [color=blue]
end_hub: goal 3 0 [color=red]

connection: start-waypoint1
connection: waypoint1-waypoint2
connection: waypoint2-goal
```

### Expected behavior

The two drones travel from `start` to `goal` along the same linear chain. Because the path is simple and not congested, both drones follow the route smoothly and reach the destination in a minimal number of turns.

The terminal output is structured similarly to:

```text
Loaded 4 zones, 2 drones
Start: start -> End: goal
Turn 1: D1-start-D2-start
Turn 2: D1-waypoint1 D2-waypoint1
Turn 3: D1-waypoint2 D2-waypoint2
Turn 4: D1-goal D2-goal
Total turns: 4
```

Depending on the exact simulation state and route scheduling, the precise movement strings may vary slightly, but the overall behavior remains the same: all drones progress toward the end hub while respecting route logic and constraints.

## Resources

### References

- [A* Search Algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Python Documentation](https://docs.python.org/3/)
- [Graph Theory Fundamentals](https://en.wikipedia.org/wiki/Graph_theory)

### AI usage

AI was used as a support tool during the development of this project for:

- explaining the architecture and the separation between parsing, routing, simulation, and visualization
- suggesting refactoring patterns for cleaner object-oriented organization
- reviewing logic around time-aware pathfinding and capacity handling
- generating technical documentation and improving readability of the code
- drafting the README structure and summarizing the algorithmic choices

AI was not used to replace the core algorithm design or the simulation logic; it was used mainly to clarify implementation decisions, improve maintainability, and produce high-quality project documentation.

## Additional notes

This project is a strong example of constrained graph simulation, combining algorithmic path planning with interactive visualization. It demonstrates how a seemingly simple movement problem quickly becomes a scheduling and concurrency challenge when multiple drones share the same infrastructure and each zone or connection has its own limits.

The repository includes several maps of increasing difficulty, from easy linear routes to highly constrained scenarios, making it well-suited for studying pathfinding robustness, coordination strategies, and display-driven debugging.
