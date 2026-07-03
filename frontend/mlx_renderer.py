"""Graphical renderer using MiniLibX (bonus).

This is a starting skeleton only. Fill in the actual MLX calls once you've
picked a Python MLX binding (e.g. `python-mlx`, a ctypes wrapper, or a
pygame-based fallback if MLX itself is unavailable on your platform).
"""

from frontend.renderer_base import MazeLike, Renderer


class MlxRenderer(Renderer):
    def __init__(self, cell_size: int = 20) -> None:
        self.cell_size = cell_size
        self._window = None

    def draw(
        self,
        maze: MazeLike,
        show_path: bool,
        wall_color: str,
        pattern_color: str = "bold_white",
    ) -> None:
        raise NotImplementedError(
            "MLX rendering not implemented yet. Use AsciiRenderer for now."
        )

    def close(self) -> None:
        if self._window is not None:
            self._window = None
