import sys
from src.parser import Parser, ParseError
from src.display import PygameDisplay
from src.simulation import SimulationEngine
from src.terminal_display import TerminalDisplay

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

    print(f"Loaded {len(drone_map.zones)} zones, {drone_map.nb_drones} drones")
    print(f"Start: {drone_map.start.name} -> End: {drone_map.end.name}")


    display = TerminalDisplay(drone_map)
    display.print_header()
    engine = SimulationEngine(drone_map)
    try:
        turns = engine.run()
    except RuntimeError as e:
        print(f"Simulation error: {e}")
        sys.exit(1)

    for i, turn_moves in enumerate(turns, start=1):
        display.print_turn(i, turn_moves)

    display.print_summary(len(turns))

    display = PygameDisplay(drone_map, engine.position_history)
    display.run()


if __name__ == "__main__":
    main()