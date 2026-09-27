"""Command-line entry point for the Fly-in simulation.

This module bootstraps the application and starts the simulation using the
selected map and display mode.
"""
import argparse
from generator import FlyInApp


def main() -> None:
    """Parse command-line options and start the application."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--capacity-info",
        action="store_true"
    )
    args = parser.parse_args()
    FlyInApp(capacity_info=args.capacity_info).run()


if __name__ == "__main__":
    main()
