from pathlib import Path
from generator import Parser, ParseError, SimulationEngine

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
BOLD = "\033[1m"
RESET = "\033[0m"

TARGETS = {
    "easy/01_linear_path.txt": 6,
    "easy/02_simple_fork.txt": 6,
    "easy/03_basic_capacity.txt": 6,
    "medium/01_dead_end_trap.txt": 12,
    "medium/02_circular_loop.txt": 20,
    "medium/03_priority_puzzle.txt": 12,
    "hard/01_maze_nightmare.txt": 20,
    "hard/02_capacity_hell.txt": 25,
    "hard/03_ultimate_challenge.txt": 30,
}


def benchmark(map_path: str, target: int) -> None:
    full_path = Path("maps") / map_path
    if not full_path.exists():
        print(f"{YELLOW}  {map_path}: file not found, skipping{RESET}")
        return

    try:
        drone_map = Parser(str(full_path)).parse()
        engine = SimulationEngine(drone_map)
        turns = engine.run()
        total = len(turns)
    except (ParseError, RuntimeError) as e:
        print(f"{RED} {map_path}: ERROR — {e}{RESET}")
        return

    if total <= target:
        status = f"{GREEN}{BOLD}OK{RESET}"
    else:
        status = f"{RED}{BOLD}NO{RESET}"

    print(f"{status} {map_path}: {total} turns (target ≤ {target})")


def main() -> None:
    print(f"{BOLD}Running benchmarks...{RESET}\n")
    for map_path, target in TARGETS.items():
        benchmark(map_path, target)


if __name__ == "__main__":
    main()
