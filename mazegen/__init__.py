"""mazegen - a small, reusable maze generation library.

Basic usage:
    >>> from mazegen import MazeGenerator
    >>> gen = MazeGenerator(20, 15, seed=42, perfect=True,
    ...                     entry=(0, 0), exit=(19, 14))
    >>> gen.generate()
    >>> walls = gen.get_walls()
    >>> path = gen.shortest_path()
"""

from .generator import FULLY_CLOSED, MazeGenerationError, MazeGenerator

__all__ = ["MazeGenerator", "MazeGenerationError", "FULLY_CLOSED"]
__version__ = "1.0.0"
