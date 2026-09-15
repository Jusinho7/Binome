"""Custom exceptions used across the Fly-in project."""

from __future__ import annotations


class FlyInError(Exception):
    """Base class for every error raised by this project."""


class MapParsingError(FlyInError):
    """Raised when the input map file is malformed.

    Attributes:
        line_number: The 1-indexed line number where the error occurred.
        raw_line: The raw content of the offending line.
        reason: A human readable explanation of the problem.
    """

    def __init__(self, line_number: int, raw_line: str, reason: str) -> None:
        self.line_number = line_number
        self.raw_line = raw_line
        self.reason = reason
        message = (
            f"Parsing error at line {line_number}: {reason}\n"
            f"  -> {raw_line.strip()!r}"
        )
        super().__init__(message)


class UnreachableDestinationError(FlyInError):
    """Raised when a drone cannot reach the end zone within the search horizon."""

    def __init__(self, drone_id: str) -> None:
        self.drone_id = drone_id
        super().__init__(
            f"Drone {drone_id} could not find a valid path to the end zone "
            "within the allotted search horizon."
        )
