from mazegen import MazeGenerator
import subprocess


_RESET = "\033[0m"

_THEMES: list[dict[str, str]] = [
    {"wall": "\033[97m", "entry": "\033[95m", "exit": "\033[91m",
     "path": "\033[96m", "pattern": "\033[90m"},
    {"wall": "\033[93m", "entry": "\033[95m", "exit": "\033[91m",
     "path": "\033[94m", "pattern": "\033[33m"},
    {"wall": "\033[92m", "entry": "\033[95m", "exit": "\033[91m",
     "path": "\033[96m", "pattern": "\033[32m"},
]

_CORNER_GLYPHS: dict[tuple[bool, bool, bool, bool], str] = {
    (True, True, True, True): "┼",
    (False, True, True, True): "┬",
    (True, False, True, True): "┴",
    (True, True, False, True): "├",
    (True, True, True, False): "┤",
    (True, True, False, False): "│",
    (False, False, True, True): "─",
    (False, True, False, True): "╭",
    (False, True, True, False): "╮",
    (True, False, False, True): "╰",
    (True, False, True, False): "╯",
    (True, False, False, False): "╵",
    (False, True, False, False): "╷",
    (False, False, True, False): "╴",
    (False, False, False, True): "╶",
    (False, False, False, False): " ",
}

_HORIZONTAL_GLYPH = "─"
_VERTICAL_GLYPH = "│"
_H_SCALE = 2


class ASCIIDisplay:
    def __init__(self, generator: MazeGenerator) -> None:
        self.generator = generator
        self._show_path = False
        self._theme_index = 0

    def render(self) -> str:
        """Return the maze rendered as a colored ASCII string."""
        width, height = self.generator.width, self.generator.height
        theme = _THEMES[self._theme_index]
        horiz, vert = self._build_edge_grids()

        path_cells: set[tuple[int, int]] = set()
        if self._show_path:
            path_cells = self._path_cell_set()

        pattern_cells = self.generator.get_pattern_cells()

        lines: list[str] = []
        for r in range(2 * height + 1):
            row_chars: list[str] = []
            for c in range(2 * width + 1):
                row_chars.append(
                    self._render_point(
                        r, c, horiz, vert, theme, pattern_cells, path_cells
                    )
                )
            lines.append("".join(row_chars))
        return "\n".join(lines)

    def _build_edge_grids(
        self,
    ) -> tuple[list[list[bool]], list[list[bool]]]:
        walls = self.generator.get_walls()
        width, height = self.generator.width, self.generator.height

        horiz = [[False] * (2 * width) for _ in range(2 * height + 1)]
        vert = [[False] * (2 * width + 1) for _ in range(2 * height)]

        for y in range(height):
            for x in range(width):
                bits = walls[y][x]
                r0, c0 = 2 * y, 2 * x
                if bits & 0b0001:  # North
                    horiz[r0][c0] = True
                    horiz[r0][c0 + 1] = True
                if bits & 0b0100:  # South
                    horiz[r0 + 2][c0] = True
                    horiz[r0 + 2][c0 + 1] = True
                if bits & 0b1000:  # West
                    vert[r0][c0] = True
                    vert[r0 + 1][c0] = True
                if bits & 0b0010:  # East
                    vert[r0][c0 + 2] = True
                    vert[r0 + 1][c0 + 2] = True

        return horiz, vert

    def _render_point(
        self,
        r: int,
        c: int,
        horiz: list[list[bool]],
        vert: list[list[bool]],
        theme: dict[str, str],
        pattern_cells: set[tuple[int, int]],
        path_cells: set[tuple[int, int]],
    ) -> str:
        wall_color = theme["wall"]
        height2, width2 = len(vert), len(horiz[0])

        if r % 2 == 0 and c % 2 == 0:
            up = r > 0 and vert[r - 1][c]
            down = r < height2 and vert[r][c]
            left = c > 0 and horiz[r][c - 1]
            right = c < width2 and horiz[r][c]
            glyph = _CORNER_GLYPHS[(up, down, left, right)]
            if glyph == " ":
                return " "
            return f"{wall_color}{glyph}{_RESET}"

        if r % 2 == 0 and c % 2 == 1:
            if horiz[r][c]:
                segment = _HORIZONTAL_GLYPH * _H_SCALE
                return f"{wall_color}{segment}{_RESET}"
            return " " * _H_SCALE

        if r % 2 == 1 and c % 2 == 0:
            if vert[r][c]:
                return f"{wall_color}{_VERTICAL_GLYPH}{_RESET}"
            return " "

        # Cell interior (odd row, odd col).
        x, y = (c - 1) // 2, (r - 1) // 2
        return self._render_interior(x, y, theme, pattern_cells, path_cells)

    def _render_interior(
        self,
        x: int,
        y: int,
        theme: dict[str, str],
        pattern_cells: set[tuple[int, int]],
        path_cells: set[tuple[int, int]],
    ) -> str:
        pad = " " * (_H_SCALE - 1)
        if (x, y) == self.generator.entry:
            return f"{theme['entry']}E{_RESET}{pad}"
        if (x, y) == self.generator.exit:
            return f"{theme['exit']}X{_RESET}{pad}"
        if (x, y) in pattern_cells:
            block = "█" * _H_SCALE
            return f"{theme['pattern']}{block}{_RESET}"
        if (x, y) in path_cells:
            return f"{theme['path']}●{_RESET}{pad}"
        return " " * _H_SCALE

    def _path_cell_set(self) -> set[tuple[int, int]]:
        directions = {
            "N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0),
        }
        x, y = self.generator.entry
        cells = {(x, y)}
        for letter in self.generator.shortest_path():
            dx, dy = directions[letter]
            x, y = x + dx, y + dy
            cells.add((x, y))
        return cells

    def run(self) -> None:
        """Run the interactive terminal menu until the user quits."""
        while True:
            print(self.render())
            print()
            print("=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")
            try:
                choice = input("Choice? (1-4): ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nBye!")
                return

            if choice == "1":
                subprocess.run(["clear"])
                self._regenerate()
            elif choice == "2":
                subprocess.run(["clear"])
                self._show_path = not self._show_path
            elif choice == "3":
                subprocess.run(["clear"])
                self._theme_index = (self._theme_index + 1) % len(_THEMES)
            elif choice == "4":
                subprocess.run(["clear"])
                print("Bye!")
                return
            else:
                subprocess.run(["clear"])
                print(
                    "Invalid choice, please enter a number between 1 and 4."
                )

    def _regenerate(self) -> None:
        old = self.generator
        new_seed = None if old.seed is None else old.seed + 1
        self.generator = MazeGenerator(
            width=old.width,
            height=old.height,
            seed=new_seed,
            perfect=old.perfect,
            entry=old.entry,
            exit=old.exit,
            embed_pattern=old.embed_pattern,
        )
        self.generator.generate()
