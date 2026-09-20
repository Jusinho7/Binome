"""Terminal rendering helpers for displaying drone simulation state."""

try:
    from rich.console import Console
except ImportError as exc:
    raise SystemExit(
        "Error: The 'rich' library is not installed. "
        "Please install it using 'pip install rich' and try again."
    ) from exc

from .models import DroneMap

console = Console()

DRONE_PALETTE = [
    "bright_cyan",
    "bright_magenta",
    "bright_yellow",
    "bright_green",
    "bright_blue",
    "bright_red",
]

ZONE_COLOR_MAP = {
    "green": "green",
    "red": "red",
    "yellow": "yellow",
    "blue": "blue",
    "gray": "grey50",
}


class TerminalDisplay:
    """Render a drone simulation in the terminal."""

    def __init__(self, drone_map: DroneMap) -> None:
        """Initialize the terminal display with a drone map."""
        self.drone_map = drone_map

    def _drone_color(self, drone_id: int) -> str:
        """Return the Rich color associated with a drone ID."""
        return DRONE_PALETTE[(drone_id - 1) % len(DRONE_PALETTE)]

    def _zone_style(self, zone_name: str) -> str:
        """Return the Rich style for the given zone name."""
        zone = self.drone_map.zones.get(zone_name)
        if zone is None:
            return "white"
        if zone.color is None:
            return "white"
        return ZONE_COLOR_MAP.get(zone.color, "white")

    def print_header(self) -> None:
        """Print the simulation header with map and drone summary."""
        start = self.drone_map.start
        end = self.drone_map.end
        if start is None or end is None:
            raise ValueError("Drone map must define start and end zones")
        console.print(
            f"[bold]Loaded[/bold] {len(self.drone_map.zones)} zones, "
            f"{self.drone_map.nb_drones} drones"
        )
        console.print(
            f"[bold green]Start[/bold green]: {start.name} -> "
            f"[bold red]End[/bold red]: {end.name}\n"
        )

    def print_turn(self, turn_number: int, moves: list[str]) -> None:
        """Print the moves executed during a simulation turn."""
        if not moves:
            console.print(f"[dim]Turn {turn_number}: (waiting)[/dim]")
            return

        parts: list[str] = []
        for move in moves:
            drone_part, destination = move.split("-", 1)
            drone_id = int(drone_part[1:])
            d_color = self._drone_color(drone_id)
            z_color = self._zone_style(destination)
            parts.append(
                f"[bold {d_color}]{drone_part}[/bold {d_color}]-"
                f"[{z_color}]{destination}[/{z_color}]"
            )

        console.print(f"[bold]Turn {turn_number}:[/bold] " + " ".join(parts))

    def print_summary(self, total_turns: int) -> None:
        """Print a final summary for the completed simulation."""
        console.print(f"\n[bold cyan]Total turns:[/bold cyan] {total_turns}")
