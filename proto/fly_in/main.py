"""Command-line entry point of the Fly-in drone routing simulator.

Usage:
    python -m fly_in.main <map_file> [--pygame] [--quiet]
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from fly_in.core.exceptions import FlyInError
from fly_in.core.parser import MapParser
from fly_in.core.simulator import Simulator
from fly_in.core.visualizer import Visualizer


def build_arg_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="fly-in",
        description="Route a fleet of drones through a zone network in the "
        "fewest possible simulation turns.",
    )
    parser.add_argument("map_file", help="Path to the map description file.")
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only print the raw turn-by-turn simulation log (no colors, "
        "no map overview, no summary).",
    )
    parser.add_argument(
        "--pygame",
        action="store_true",
        help="Open an animated Pygame window showing the network and drones.",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Run the CLI. Returns the process exit code."""
    args = build_arg_parser().parse_args(argv)

    try:
        drone_map = MapParser().parse_file(args.map_file)
    except FlyInError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    except OSError as error:
        print(f"Error: could not read {args.map_file!r}: {error}", file=sys.stderr)
        return 1

    simulator = Simulator(drone_map)

    try:
        result = simulator.run()
    except FlyInError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    if args.quiet:
        print(result.render())
        return 0

    visualizer = Visualizer(drone_map)
    if args.pygame:
        try:
            visualizer.show_pygame(result)
        except ImportError:
            print(
                "Error: Pygame is required for --pygame. "
                "Install it with: python -m pip install pygame",
                file=sys.stderr,
            )
            return 1
        return 0

    visualizer.print_map_summary()
    visualizer.print_simulation(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
