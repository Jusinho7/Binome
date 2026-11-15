"""JSON file reading helper."""
import json
from pathlib import Path
from typing import Any


def read_json(path: str | Path) -> Any:
    """Read and parse a JSON file.

    Args:
        path: path of the JSON file.

    Returns:
        The parsed JSON content.

    Raises:
        ValueError: if the file is missing, unreadable or invalid JSON.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as error:
        raise ValueError(f"File not found: {path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {path}: {error}") from error
    except OSError as error:
        raise ValueError(f"Cannot read {path}: {error}") from error
