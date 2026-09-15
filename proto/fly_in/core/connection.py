"""Connection model: a bidirectional edge linking two zones."""

from __future__ import annotations


class Connection:
    """A bidirectional link between two zones.

    Attributes:
        zone_a: Name of the first endpoint.
        zone_b: Name of the second endpoint.
        max_link_capacity: Maximum number of drones allowed to traverse
            this connection during the same simulation turn.
    """

    def __init__(self, zone_a: str, zone_b: str, max_link_capacity: int = 1) -> None:
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity

    @property
    def name(self) -> str:
        """The canonical, file-order name of this connection, e.g. ``a-b``."""
        return f"{self.zone_a}-{self.zone_b}"

    def other_end(self, zone_name: str) -> str:
        """Return the endpoint of this connection opposite ``zone_name``.

        Args:
            zone_name: One of the two endpoints of this connection.

        Returns:
            The name of the other endpoint.

        Raises:
            ValueError: If ``zone_name`` is not an endpoint of this connection.
        """
        if zone_name == self.zone_a:
            return self.zone_b
        if zone_name == self.zone_b:
            return self.zone_a
        raise ValueError(
            f"Zone {zone_name!r} is not an endpoint of connection {self.name!r}."
        )

    def connects(self, zone_a: str, zone_b: str) -> bool:
        """Whether this connection links the (unordered) pair given."""
        return {zone_a, zone_b} == {self.zone_a, self.zone_b}

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"Connection({self.name}, capacity={self.max_link_capacity})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Connection):
            return NotImplemented
        return {self.zone_a, self.zone_b} == {other.zone_a, other.zone_b}

    def __hash__(self) -> int:
        return hash(frozenset((self.zone_a, self.zone_b)))
