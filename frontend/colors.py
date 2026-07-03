"""Color palettes shared by all renderers.

ANSI codes are used for the terminal renderer; the same keys map to
RGB-ish hex/int values that an MLX renderer could reuse later.
"""

from typing import Final

ANSI_RESET: Final[str] = "\033[0m"

WALL_COLOR_CYCLE: Final[list[str]] = [
    "white", "yellow", "cyan", "green", "magenta",
]

ANSI_COLORS: Final[dict[str, str]] = {
    "white": "\033[97m",
    "yellow": "\033[93m",
    "cyan": "\033[96m",
    "green": "\033[92m",
    "magenta": "\033[95m",
    "red": "\033[91m",
    "blue": "\033[94m",
    "bold_white": "\033[1;97m",
    "bold_yellow": "\033[1;93m",
    "bold_red": "\033[1;91m",
    "bold_cyan": "\033[1;96m",
}

PATTERN_42_COLOR_CYCLE: Final[list[str]] = [
    "bold_white", "bold_yellow", "bold_red", "bold_cyan",
]

ROLE_COLORS: Final[dict[str, str]] = {
    "entry": "magenta",
    "exit": "red",
    "path": "blue",
}


def ansi(color_name: str) -> str:
    return ANSI_COLORS.get(color_name, "")


def next_in_cycle(current: str, cycle: list[str]) -> str:
    try:
        idx = cycle.index(current)
    except ValueError:
        return cycle[0]
    return cycle[(idx + 1) % len(cycle)]


def next_color(current: str) -> str:
    return next_in_cycle(current, WALL_COLOR_CYCLE)


def next_pattern_color(current: str) -> str:
    return next_in_cycle(current, PATTERN_42_COLOR_CYCLE)
