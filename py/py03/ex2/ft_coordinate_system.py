import math


def get_player_pos() -> tuple[float, float, float]:
    while True:
        raw: str = input("Enter new coordinates as floats in format 'x,y,z': ")
        parts: list[str] = raw.split(",")
        if len(parts) != 3:
            print("Invalid syntax")
            continue
        coords: list[float] = []
        valid: bool = True
        for part in parts:
            try:
                coords.append(float(part.strip()))
            except ValueError as e:
                print(f"Error on parameter '{part.strip()}': {e}")
                valid = False
                break
        if valid:
            return (coords[0], coords[1], coords[2])


def distance(
    p1: tuple[float, float, float],
    p2: tuple[float, float, float]
) -> float:
    return math.sqrt(
        (p2[0] - p1[0]) ** 2 +
        (p2[1] - p1[1]) ** 2 +
        (p2[2] - p1[2]) ** 2
    )


def main() -> None:
    print("=== Game Coordinate System ===")

    print("Get a first set of coordinates")
    pos1: tuple[float, float, float] = get_player_pos()
    print(f"Got a first tuple: {pos1}")
    print(f"It includes: X={pos1[0]}, Y={pos1[1]}, Z={pos1[2]}")
    dist_center: float = distance(pos1, (0.0, 0.0, 0.0))
    print(f"Distance to center: {round(dist_center, 4)}")

    print("\nGet a second set of coordinates")
    pos2: tuple[float, float, float] = get_player_pos()
    dist_between: float = distance(pos1, pos2)
    print(
        f"Distance between the 2 sets of coordinates: {round(dist_between, 4)}"
    )


if __name__ == "__main__":
    main()
