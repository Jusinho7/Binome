"""Command-line entry point for the Fly-in simulation.

This module bootstraps the application and starts the simulation using the
selected map and display mode.
"""

from generator import FlyInApp


def main() -> None:
    """Compatibility wrapper around the application object."""
    FlyInApp().run()


if __name__ == "__main__":
    main()
