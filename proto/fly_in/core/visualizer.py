"""Terminal and Pygame visualisation of the map and simulation log.

Only raw ANSI escape codes are used so that the project has zero
external dependency for its mandatory visual feedback requirement.
"""

from __future__ import annotations

from typing import Dict, Optional

from fly_in.core.graph_map import DroneMap
from fly_in.core.simulator import SimulationResult
from fly_in.core.zone import ZoneType

_RESET = "\033[0m"
_BOLD = "\033[1m"

# Fallback palette used for named colors coming from the map file, plus a
# dedicated color per zone type so the layout stays readable even when the
# map does not specify any `color=` tag.
_NAMED_COLORS: Dict[str, str] = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "gray": "\033[90m",
    "grey": "\033[90m",
}

_ZONE_TYPE_COLORS: Dict[ZoneType, str] = {
    ZoneType.NORMAL: "\033[37m",
    ZoneType.PRIORITY: "\033[32m",
    ZoneType.RESTRICTED: "\033[33m",
    ZoneType.BLOCKED: "\033[90m",
}

_DRONE_PALETTE = [
    "\033[91m", "\033[92m", "\033[93m", "\033[94m",
    "\033[95m", "\033[96m", "\033[31m", "\033[32m",
]


class Visualizer:
    """Displays a colored overview of the map and simulation log."""

    def __init__(self, drone_map: DroneMap) -> None:
        self._map = drone_map

    def _color_for_zone(self, zone_name: str) -> str:
        zone = self._map.get_zone(zone_name)
        if zone.color and zone.color.lower() in _NAMED_COLORS:
            return _NAMED_COLORS[zone.color.lower()]
        return _ZONE_TYPE_COLORS.get(zone.zone_type, "")

    def print_map_summary(self) -> None:
        """Print a colored textual summary of every zone in the map."""
        print(f"{_BOLD}== Network overview =={_RESET}")
        for zone in self._map.zones.values():
            color = self._color_for_zone(zone.name)
            tag = "[START]" if zone.is_start else "[END]" if zone.is_end else ""
            print(
                f"  {color}{zone.name:<12}{_RESET} "
                f"({zone.x}, {zone.y})  type={zone.zone_type.value:<10} "
                f"capacity={zone.max_drones}  {tag}"
            )
        print(f"{_BOLD}== Connections =={_RESET}")
        for connection in self._map.connections:
            print(
                f"  {connection.zone_a} <-> {connection.zone_b} "
                f"(capacity={connection.max_link_capacity})"
            )
        print()

    def print_simulation(self, result: SimulationResult) -> None:
        """Print the turn-by-turn simulation log with colored drone tags."""
        print(f"{_BOLD}== Simulation =={_RESET}")
        drone_colors: Dict[str, str] = {}
        for turn_log in result.turns:
            if not turn_log.actions:
                continue
            rendered_actions = []
            for action in turn_log.actions:
                drone_label = action.split("-", 1)[0]
                color = self._color_for_drone(drone_label, drone_colors)
                rendered_actions.append(f"{color}{action}{_RESET}")
            print(f"  T{turn_log.turn:<4}| " + " ".join(rendered_actions))
        print()
        self.print_summary(result)

    def _color_for_drone(self, drone_label: str, cache: Dict[str, str]) -> str:
        if drone_label not in cache:
            cache[drone_label] = _DRONE_PALETTE[len(cache) % len(_DRONE_PALETTE)]
        return cache[drone_label]

    def print_summary(self, result: SimulationResult, record: Optional[int] = None) -> None:
        """Print the aggregate performance metrics of a simulation result."""
        print(f"{_BOLD}== Summary =={_RESET}")
        print(f"  Total simulation turns : {result.total_turns}")
        print(f"  Drones delivered       : {result.drones_delivered}")
        print(f"  Total path cost        : {result.total_path_cost}")
        print(f"  Average turns / drone  : {result.average_turns_per_drone:.2f}")
        if record is not None:
            verdict = "beaten!" if result.total_turns < record else "not beaten"
            print(f"  Reference record       : {record} turns ({verdict})")

    def show_pygame(self, result: SimulationResult) -> None:
        """Animate the simulation in a Pygame window until the user quits."""
        import pygame  # type: ignore[import-not-found]

        pygame.init()
        try:
            width, height = 1100, 760
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            pygame.display.set_caption("Fly-in | Drone routing")
            clock = pygame.time.Clock()
            title_font = pygame.font.Font(None, 30)
            label_font = pygame.font.Font(None, 20)
            drone_font = pygame.font.Font(None, 18)
            positions = self._pygame_positions(width, height)
            drone_positions = {
                f"D{drone_id}": self._map.start_zone_name
                for drone_id in range(1, self._map.nb_drones + 1)
            }
            drone_colors = {
                label: _pygame_drone_color(index)
                for index, label in enumerate(drone_positions)
            }
            current_turn = 0
            elapsed = 0.0
            paused = False
            running = True

            while running:
                delta = clock.tick(60) / 1000.0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            paused = not paused
                        elif event.key == pygame.K_RIGHT and current_turn < result.total_turns:
                            current_turn += 1
                            self._apply_pygame_turn(result, current_turn, drone_positions)
                        elif event.key == pygame.K_ESCAPE:
                            running = False

                if not paused and current_turn < result.total_turns:
                    elapsed += delta
                    if elapsed >= 0.65:
                        elapsed = 0.0
                        current_turn += 1
                        self._apply_pygame_turn(result, current_turn, drone_positions)

                screen.fill((18, 24, 33))
                self._draw_pygame_network(screen, positions, label_font)
                self._draw_pygame_drones(
                    screen, positions, drone_positions, drone_colors, drone_font
                )
                title = title_font.render(
                    f"Fly-in   Tour {current_turn}/{result.total_turns}",
                    True,
                    (238, 242, 247),
                )
                screen.blit(title, (28, 22))
                status = "PAUSE" if paused else (
                    "TERMINE" if current_turn >= result.total_turns else "EN COURS"
                )
                status_surface = label_font.render(
                    f"{status}   [Espace] pause   [Echap] quitter",
                    True,
                    (166, 180, 194),
                )
                screen.blit(status_surface, (30, 55))
                pygame.display.flip()
        finally:
            pygame.quit()

    def _pygame_positions(self, width: int, height: int) -> Dict[str, tuple[int, int]]:
        margin = 90
        usable_width = max(width - 2 * margin, 1)
        usable_height = max(height - 2 * margin, 1)
        xs = [zone.x for zone in self._map.zones.values()]
        ys = [zone.y for zone in self._map.zones.values()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        def scale(value: int, lower: int, upper: int, size: int) -> int:
            if lower == upper:
                return size // 2
            return margin + int((value - lower) * size / (upper - lower))

        return {
            zone.name: (
                scale(zone.x, min_x, max_x, usable_width),
                height - scale(zone.y, min_y, max_y, usable_height),
            )
            for zone in self._map.zones.values()
        }

    def _draw_pygame_network(
        self,
        screen: object,
        positions: Dict[str, tuple[int, int]],
        label_font: object,
    ) -> None:
        import pygame  # type: ignore[import-not-found]

        for connection in self._map.connections:
            start = positions[connection.zone_a]
            end = positions[connection.zone_b]
            pygame.draw.line(screen, (70, 88, 106), start, end, 4)
            midpoint = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
            capacity = label_font.render(
                str(connection.max_link_capacity), True, (120, 137, 153)
            )
            screen.blit(capacity, midpoint)

        for zone in self._map.zones.values():
            color = _pygame_zone_color(zone)
            pygame.draw.circle(screen, color, positions[zone.name], 25)
            pygame.draw.circle(screen, (235, 240, 245), positions[zone.name], 25, 2)
            label = label_font.render(zone.name, True, (238, 242, 247))
            screen.blit(
                label,
                (
                    positions[zone.name][0] - label.get_width() // 2,
                    positions[zone.name][1] + 32,
                ),
            )

    def _draw_pygame_drones(
        self,
        screen: object,
        positions: Dict[str, tuple[int, int]],
        drone_positions: Dict[str, str],
        drone_colors: Dict[str, tuple[int, int, int]],
        drone_font: object,
    ) -> None:
        import pygame  # type: ignore[import-not-found]

        for index, (label, zone_name) in enumerate(drone_positions.items()):
            x, y = positions[zone_name]
            offset = ((index % 3) - 1) * 16
            pygame.draw.circle(screen, drone_colors[label], (x + offset, y - 8), 10)
            text = drone_font.render(label, True, (255, 255, 255))
            screen.blit(text, (x + offset - text.get_width() // 2, y - 33))

    def _apply_pygame_turn(
        self,
        result: SimulationResult,
        turn: int,
        drone_positions: Dict[str, str],
    ) -> None:
        if turn == 0 or turn > len(result.turns):
            return
        for action in result.turns[turn - 1].actions:
            drone_label, destination = action.split("-", 1)
            if destination in self._map.zones:
                drone_positions[drone_label] = destination


def _pygame_zone_color(zone: object) -> tuple[int, int, int]:
    from fly_in.core.zone import ZoneType

    if getattr(zone, "is_start"):
        return (42, 154, 112)
    if getattr(zone, "is_end"):
        return (213, 93, 71)
    colors = {
        ZoneType.NORMAL: (67, 108, 145),
        ZoneType.PRIORITY: (45, 151, 103),
        ZoneType.RESTRICTED: (194, 137, 48),
        ZoneType.BLOCKED: (78, 86, 96),
    }
    return colors[getattr(zone, "zone_type")]


def _pygame_drone_color(index: int) -> tuple[int, int, int]:
    palette = [
        (80, 190, 235), (238, 174, 82), (226, 105, 120),
        (177, 125, 235), (107, 205, 145), (240, 220, 92),
    ]
    return palette[index % len(palette)]
