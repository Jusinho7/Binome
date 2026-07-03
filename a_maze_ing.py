"""A-Maze-ing entry point.

NOTE: This currently wires the frontend to a MockMaze so it can be run
and tested standalone. Once the backend's real MazeGenerator (and its
config-file parsing) is ready, swap the import below:

    from backend.maze_generator import MazeGenerator
    maze = MazeGenerator.from_config(config_path)

Everything else (renderer, controller) stays untouched, since both only
depend on the MazeLike interface defined in frontend/renderer_base.py.
"""

import sys

from frontend.ascii_renderer import AsciiRenderer
from frontend.controller import MazeController
from frontend.mock_maze import MockMaze


def main() -> None:
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.txt"
    print(f"[frontend] Using config: {config_path} (mock backend for now)")
    maze = MockMaze(width=15, height=10, entry=(0, 0), exit=(14, 9), seed=42)
    renderer = AsciiRenderer()
    controller = MazeController(maze, renderer)
    controller.run()


if __name__ == "__main__":
    main()
