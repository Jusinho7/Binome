#!/usr/bin/env python3
"""A-Maze-ing: config-driven maze generator with ASCII terminal display.

Usage:
    python3 a_maze_ing.py config.txt
"""

import sys

from config import ConfigError, MazeConfig, load_config
from display import ASCIIDisplay
from mazegen import MazeGenerationError, MazeGenerator
from output_writer import write_maze_file


def build_generator(cfg: MazeConfig) -> MazeGenerator:
    """Create and run a :class:`MazeGenerator` from a validated config."""
    generator = MazeGenerator(
        width=cfg.width,
        height=cfg.height,
        seed=cfg.seed,
        perfect=cfg.perfect,
        entry=cfg.entry,
        exit=cfg.exit,
    )
    generator.generate()
    return generator


def main(argv: list[str]) -> int:
    """Program entry point.

    Args:
        argv: Command-line arguments (excluding the program name).

    Returns:
        Process exit code (0 on success, 1 on error).
    """
    if len(argv) != 1:
        print("Usage: python3 a_maze_ing.py <config_file>", file=sys.stderr)
        return 1

    config_path = argv[0]

    try:
        cfg = load_config(config_path)
    except ConfigError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 1

    try:
        generator = build_generator(cfg)
    except MazeGenerationError as exc:
        print(f"Maze generation error: {exc}", file=sys.stderr)
        return 1

    try:
        write_maze_file(cfg.output_file, generator)
    except OSError as exc:
        print(
            f"Could not write output file '{cfg.output_file}': {exc}",
            file=sys.stderr,
        )
        return 1

    print(f"Maze written to '{cfg.output_file}'.")

    try:
        ASCIIDisplay(generator).run()
    except Exception as exc:  # noqa: BLE001 - never crash on display issues
        print(f"Display error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
