"""Interactive controller driving the maze display loop.

Works with any Renderer implementation (ASCII, MLX, ...) thanks to the
common Renderer interface, and with any backend object satisfying the
MazeLike protocol.
"""

from frontend.colors import WALL_COLOR_CYCLE, PATTERN_42_COLOR_CYCLE
from frontend.colors import next_color, next_pattern_color
from frontend.renderer_base import MazeLike, Renderer

MENU_TEXT = (
    "\n=== A-Maze-ing ===\n"
    "1. Re-generate a new maze\n"
    "2. Show/Hide path from entry to exit\n"
    "3. Rotate maze colors\n"
    "4. Quit\n"
    "5. Rotate '42' pattern color\n"
)


class MazeController:
    def __init__(self, maze: MazeLike, renderer: Renderer) -> None:
        self.maze = maze
        self.renderer = renderer
        self.show_path = False
        self.wall_color = WALL_COLOR_CYCLE[0]
        self.pattern_color = PATTERN_42_COLOR_CYCLE[0]

    def run(self) -> None:
        self._draw()
        while True:
            print(MENU_TEXT)
            choice = input("Choice? (1-5): ").strip()
            try:
                if not self._handle_choice(choice):
                    break
            except (AttributeError, ValueError) as exc:
                print(f"[frontend] Action failed: {exc}")
        self.renderer.close()

    def _draw(self) -> None:
        self.renderer.draw(
            self.maze, self.show_path, self.wall_color, self.pattern_color
        )

    def _handle_choice(self, choice: str) -> bool:
        if choice == "1":
            self.maze.regenerate()
            self._draw()
        elif choice == "2":
            self.show_path = not self.show_path
            self._draw()
        elif choice == "3":
            self.wall_color = next_color(self.wall_color)
            self._draw()
        elif choice == "4":
            return False
        elif choice == "5":
            self.pattern_color = next_pattern_color(self.pattern_color)
            self._draw()
        else:
            print("Invalid choice, please enter a number between 1 and 5.")
        return True
