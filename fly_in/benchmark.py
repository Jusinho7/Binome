"""Run the benchmark suite for the fly-in maps."""

from pathlib import Path
from generator import Parser, ParseError, SimulationEngine

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
BOLD = "\033[1m"
RESET = "\033[0m"

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

    def run(self) -> None:
        """Execute the benchmark matrix."""
        print(f"{BOLD}Running benchmarks...{RESET}\n")
        for map_path, target in self.targets.items():
            self.benchmark(map_path, target)

    def benchmark(self, map_path: str, target: int) -> None:
        """Benchmark one map against a target number of turns."""
        full_path = Path("maps") / map_path
        if not full_path.exists():
            print(f"{YELLOW}  {map_path}: file not found, skipping{RESET}")
            return

        try:
            drone_map = Parser(str(full_path)).parse()
            engine = SimulationEngine(drone_map)
            turns = engine.run()
            total = len(turns)
        except (ParseError, RuntimeError) as exc:
            print(f"{RED} {map_path}: ERROR — {exc}{RESET}")
            return

        status = self._format_status(total, target)
        print(f"{status} {map_path}: {total} turns (target ≤ {target})")

    @staticmethod
    def _format_status(total_turns: int, target: int) -> str:
        """Return the colored benchmark status for a result."""
        if total_turns <= target:
            return f"{GREEN}{BOLD}OK{RESET}"
        return f"{RED}{BOLD}NO{RESET}"


def main() -> None:
    """Compatibility wrapper for the benchmark runner."""
    BenchmarkRunner(TARGETS).run()


if __name__ == "__main__":
    main()
