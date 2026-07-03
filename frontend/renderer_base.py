"""Abstract base class defining the common renderer interface.

Any concrete renderer (ASCII terminal, MLX graphical, ...) must implement
this interface so the controller can switch between them transparently.
"""

from abc import ABC, abstractmethod
from typing import Protocol


class MazeLike(Protocol):
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]

    def get_walls(self, x: int, y: int) -> int: ...
    def get_solution_path(self) -> list[str]: ...
    def regenerate(self, seed: int | None = None) -> None: ...


class Renderer(ABC):
    @abstractmethod
    def draw(
        self,
        maze: MazeLike,
        show_path: bool,
        wall_color: str,
        pattern_color: str = "bold_white",
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError
