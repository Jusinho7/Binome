NORTH, EAST, SOUTH, WEST = "N", "E", "S", "W"

DIRECTIONS: dict[str, tuple[int, int, int]] = {
    NORTH: (0, -1, 0b0001),
    EAST: (1, 0, 0b0010),
    SOUTH: (0, 1, 0b0100),
    WEST: (-1, 0, 0b1000),
}

OPPOSITE: dict[str, str] = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}

FULLY_CLOSED = 0b1111
