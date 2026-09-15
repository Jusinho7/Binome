import sys
from src.parser import Parser, ParseError
from src.display import PygameDisplay


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python main.py <map_file>")
        sys.exit(1)

    try:
        drone_map = Parser(sys.argv[1]).parse()
    except ParseError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Loaded {len(drone_map.zones)} zones, {drone_map.nb_drones} drones")
    print(f"Start: {drone_map.start.name} -> End: {drone_map.end.name}")

    display = PygameDisplay(drone_map)
    display.run()


if __name__ == "__main__":
    main()