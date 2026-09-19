import sys
from generator import (
    Parser, ParseError, SimulationEngine, TerminalDisplay, PygameDisplay
)

RED = "\033[31m"
RESET = "\033[0m"


def main() -> None:
    if len(sys.argv) != 2:
        print(f"{RED}Usage: python main.py <map_file>{RESET}")
        sys.exit(1)

    try:
        drone_map = Parser(sys.argv[1]).parse()
    except (ParseError, FileNotFoundError) as e:
        print(f"{RED}Error: {e}{RESET}")
        sys.exit(1)

    start = drone_map.start
    end = drone_map.end
    if start is None or end is None:
        raise ValueError("Map must define a start and end hub")

    print(f"Loaded {len(drone_map.zones)} zones, {drone_map.nb_drones} drones")
    print(f"Start: {start.name} -> End: {end.name}")

    terminal_display = TerminalDisplay(drone_map)
    terminal_display.print_header()
    engine = SimulationEngine(drone_map)
    try:
        turns = engine.run()
    except RuntimeError as e:
        print(f"Simulation error: {e}")
        sys.exit(1)

    for i, turn_moves in enumerate(turns, start=1):
        terminal_display.print_turn(i, turn_moves)

    terminal_display.print_summary(len(turns))

    pygame_display = PygameDisplay(drone_map, engine.position_history, turns)
    pygame_display.run()


if __name__ == "__main__":
    main()
