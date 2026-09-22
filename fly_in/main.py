"""Entry point for the Fly-in simulation."""

import sys
from pathlib import Path
from subprocess import run
from time import sleep

from generator import (
    DroneMap,
    Parser,
    ParseError,
    PygameDisplay,
    SimulationEngine,
    TerminalDisplay,
    choice_map,
)

RED = "\033[31m"
RESET = "\033[0m"
ORANGE = "\033[33m"


class FlyInApp:
    """Orchestrate map selection, simulation and display."""

    def run(self) -> None:
        """Run the full simulation workflow."""
        maps_file = self._choose_map()
        if maps_file is None:
            self._exit_no_map_selected()
        assert maps_file is not None

        self._clear_screen()
        drone_map = self._load_map(maps_file)
        self._validate_map(drone_map)

        terminal_display = TerminalDisplay(drone_map)
        terminal_display.print_header()

        engine = SimulationEngine(drone_map)
        turns = self._run_simulation(engine)

        for i, turn_moves in enumerate(turns, start=1):
            terminal_display.print_turn(i, turn_moves)

        terminal_display.print_summary(len(turns))

        pygame_display = PygameDisplay(
            drone_map, engine.position_history, turns
        )
        pygame_display.run()

    def _choose_map(self) -> Path | None:
        """Prompt the user to choose a map file."""
        try:
            return choice_map()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{ORANGE}Exiting, user interrupted.{RESET}")
            sys.exit(1)

    def _clear_screen(self) -> None:
        """Reset the terminal screen."""
        run(["clear"])

    def _load_map(self, maps_file: Path) -> DroneMap:
        """Load and parse the selected map file."""
        try:
            return Parser(str(maps_file)).parse()
        except (ParseError, FileNotFoundError) as exc:
            print(f"{RED}Error: {exc}{RESET}")
            sys.exit(1)

    def _validate_map(self, drone_map: DroneMap) -> None:
        """Ensure the map contains a valid start and end hub."""
        start = drone_map.start
        end = drone_map.end
        if start is None or end is None:
            raise ValueError("Map must define a start and end hub")

        print(
            f"Loaded {len(drone_map.zones)} zones,"
            f" {drone_map.nb_drones} drones"
        )
        print(f"Start: {start.name} -> End: {end.name}")

    def _run_simulation(self, engine: SimulationEngine) -> list[list[str]]:
        """Execute the simulation until completion."""
        try:
            return engine.run()
        except RuntimeError as exc:
            print(f"Simulation error: {exc}")
            sys.exit(1)

    def _exit_no_map_selected(self) -> None:
        """Exit cleanly when no map was chosen."""
        print(f"{RED}No map selected. Exiting.{RESET}")
        sleep(1)
        self._clear_screen()
        sys.exit(1)


def main() -> None:
    """Compatibility wrapper around the application object."""
    FlyInApp().run()


if __name__ == "__main__":
    main()
