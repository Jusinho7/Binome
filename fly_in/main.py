"""Command-line entry point for the Fly-in simulation.

This module bootstraps the application and starts the simulation using the
selected map and display mode.
"""
from fly_in import FlyInApp


def main() -> None:
    """Parse command-line options and start the application."""
    FlyInApp().run()


if __name__ == "__main__":
    main()
