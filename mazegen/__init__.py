"""Provide the public interface for the maze generation package."""

from .maze_generator import MazeGenerator, MazeGenerationError
from .directions import NORTH, EAST, SOUTH, WEST
from .config import ConfigError, MazeConfig, load_config

__all__ = [
    "MazeGenerator",
    "MazeGenerationError",
    "NORTH",
    "EAST",
    "SOUTH",
    "WEST",
    "ConfigError",
    "MazeConfig",
    "load_config"
]
__version__ = "1.0.0"
