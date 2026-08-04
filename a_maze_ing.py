"""Run the maze generator application."""

import sys
from display import ASCIIDisplay
try:
    from mazegen import (
        MazeGenerationError,
        MazeGenerator,
        ConfigError,
        MazeConfig,
        load_config
    )
except ModuleNotFoundError:
    print("Module not found")
    sys.exit()
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
    """Run the maze generator application.

    Parse the command-line arguments, load the configuration, generate
    the maze, write it to the output file, and display the result.

    Return:
        ``0`` if the program completes successfully, otherwise ``1``.
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
    except (OSError, KeyError, IndexError) as exc:
        print(f"Display error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
