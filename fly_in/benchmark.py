"""Run the benchmark suite for the fly-in maps."""

from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from generator import Parser, ParseError, SimulationEngine

TARGETS = {
    "easy/01_linear_path.txt": 6,
    "easy/02_simple_fork.txt": 8,
    "easy/03_basic_capacity.txt": 6,
    "medium/01_dead_end_trap.txt": 12,
    "medium/02_circular_loop.txt": 15,
    "medium/03_priority_puzzle.txt": 12,
    "hard/01_maze_nightmare.txt": 30,
    "hard/02_capacity_hell.txt": 35,
    "hard/03_ultimate_challenge.txt": 45,
}


class BenchmarkRunner:
    """Run and report benchmark results for each map in the project."""

    def __init__(self, targets: dict[str, int]) -> None:
        """Initialize the benchmark runner with target thresholds."""
        self.targets = targets
        self.console = Console()

    def run(self) -> None:
        """Execute the benchmark matrix."""
        self.console.print(
            Panel.fit(
                "[bold cyan]Fly-in benchmark[/bold cyan]",
                subtitle="[dim]simulator performance report[/dim]",
            )
        )

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Map", style="cyan")
        table.add_column("Turns", justify="right", style="green")
        table.add_column("Target", justify="right", style="yellow")
        table.add_column("Status", justify="center")

        for map_path, target in self.targets.items():
            result = self.benchmark(map_path, target)
            if result is None:
                continue
            total_turns, status = result
            table.add_row(
                map_path,
                str(total_turns),
                str(target),
                status,
            )

        self.console.print(table)

    def benchmark(self, map_path: str, target: int) -> tuple[int, Text] | None:
        """Benchmark one map against a target number of turns."""
        full_path = Path("maps") / map_path
        if not full_path.exists():
            self.console.print(
                f"[yellow]  {map_path}: file not found, skipping[/yellow]"
            )
            return None

        try:
            drone_map = Parser(str(full_path)).parse()
            engine = SimulationEngine(drone_map)
            turns = engine.run()
            total = len(turns)
        except (ParseError, RuntimeError) as exc:
            self.console.print(
                f"[red]{map_path}: ERROR — {exc}[/red]"
            )
            return None

        status = self._format_status(total, target)
        return total, status

    @staticmethod
    def _format_status(total_turns: int, target: int) -> Text:
        """Return the Rich status badge for a result."""
        if total_turns <= target:
            return Text("OK", style="bold green")
        return Text("NO", style="bold red")


def main() -> None:
    """Compatibility wrapper for the benchmark runner."""
    BenchmarkRunner(TARGETS).run()


if __name__ == "__main__":
    main()
