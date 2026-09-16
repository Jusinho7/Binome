import os
import sys
RED = "\033[31m"
RESET = "\033[0m"
try:
    import pygame
except ModuleNotFoundError:
    print(
        f"{RED}Error: The 'pygame' library is not installed.{RESET}"
        f"{RED}Please install it using 'pip install pygame' and try again.{RESET}"
    )
    sys.exit()
from .models import DroneMap, Zone

WINDOW_SIZE = (1920, 1070)
BACKGROUND_IMAGE = "assets/bc.jpg"
DRONE_IMAGE = "assets/drone.png"
STATION_IMAGE = "assets/hubs/station.png"
START_IMAGE = "assets/hubs/start_stop.png"
END_IMAGE = "assets/hubs/start_stop.png"
COLORS = {
    "green": (0, 200, 0),
    "red": (200, 0, 0),
    "yellow": (220, 200, 0),
    "blue": (0, 100, 200),
    "gray": (120, 120, 120),
    "purple": (150, 0, 150),
    "orange": (255, 140, 0),
    "pink": (255, 105, 180),
    "brown": (139, 69, 19),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "lime": (0, 255, 0),
    "teal": (0, 128, 128),
    "navy": (0, 0, 128),
    "maroon": (128, 0, 0),
    "olive": (128, 128, 0),
    "silver": (192, 192, 192),
    "gold": (255, 215, 0),
    "beige": (245, 245, 220),
    "lavender": (230, 230, 250),
    "coral": (255, 127, 80),
    "salmon": (250, 128, 114),
    "khaki": (240, 230, 140),
    "plum": (221, 160, 221),
    "orchid": (218, 112, 214),
    "turquoise": (64, 224, 208),
    "indigo": (75, 0, 130),
    "violet": (238, 130, 238),
    "peach": (255, 218, 185),
    "mint": (189, 252, 201),
    "cream": (255, 253, 208),
    "tan": (210, 180, 140),
    "chocolate": (210, 105, 30),
    "charcoal": (54, 69, 79),
    "burgundy": (128, 0, 32),
    "mustard": (255, 219, 88),
    "rust": (183, 65, 14),
    "sienna": (160, 82, 45),
    "amber": (255, 191, 0),
    "cerulean": (42, 82, 190),
    "periwinkle": (204, 204, 255),
    "fuchsia": (255, 0, 255),
    None: (100, 100, 100),
}
ZONE_RADIUS = 25


class PygameDisplay:
    """Renders the drone network and replays the simulation turns."""

    def __init__(self, drone_map: DroneMap, position_history: list[dict[int, Zone]]) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.background = pygame.transform.smoothscale(
            pygame.image.load(BACKGROUND_IMAGE).convert(),
            WINDOW_SIZE
        )
        drone_image = pygame.image.load(DRONE_IMAGE).convert_alpha()
        self.drone_image = pygame.transform.smoothscale(drone_image, (72, 48))
        self.station_image = None
        if os.path.exists(STATION_IMAGE):
            station_image = pygame.image.load(STATION_IMAGE).convert_alpha()
            self.station_image = pygame.transform.smoothscale(station_image, (64, 64))
        self.start_image = self._load_hub_image(START_IMAGE)
        self.end_image = self._load_hub_image(END_IMAGE)
        pygame.display.set_caption("Fly-in — Map Preview")
        self.font = pygame.font.SysFont("consolas", 14)
        self.drone_map = drone_map
        self.position_history = position_history
        self._compute_layout()

    def _load_hub_image(self, image_path: str) -> pygame.Surface | None:
        if not os.path.exists(image_path):
            return self.station_image
        image = pygame.image.load(image_path).convert_alpha()
        return pygame.transform.smoothscale(image, (64, 64))

    def _compute_layout(self) -> None:
        """Maps zone (x, y) coordinates to screen pixel positions."""
        xs = [z.x for z in self.drone_map.zones.values()]
        ys = [z.y for z in self.drone_map.zones.values()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        margin = 80
        span_x = (max_x - min_x) or 1
        span_y = (max_y - min_y) or 1

        self.positions: dict[str, tuple[int, int]] = {}
        for zone in self.drone_map.zones.values():
            px = margin + (zone.x - min_x) / span_x * (WINDOW_SIZE[0] - 2 * margin)
            py = margin + (zone.y - min_y) / span_y * (WINDOW_SIZE[1] - 2 * margin)
            self.positions[zone.name] = (int(px), int(py))

    def _draw_frame(self, positions: dict[int, Zone]) -> None:
        self.screen.blit(self.background, (0, 0))

        overlay = pygame.Surface(WINDOW_SIZE)
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        for conn in self.drone_map.connections:
            p1 = self.positions[conn.zone_a.name]
            p2 = self.positions[conn.zone_b.name]
            pygame.draw.line(self.screen, (100, 100, 100), p1, p2, 2)

        for zone in self.drone_map.zones.values():
            pos = self.positions[zone.name]
            color = COLORS.get(zone.color, COLORS[None])
            hub_image = self.station_image
            if zone is self.drone_map.start:
                hub_image = self.start_image
            elif zone is self.drone_map.end:
                hub_image = self.end_image

            if hub_image is None:
                pygame.draw.circle(self.screen, color, pos, ZONE_RADIUS)
            else:
                station = hub_image.copy()
                station.fill((*color, 255), special_flags=pygame.BLEND_RGBA_MULT)
                station_rect = station.get_rect(center=pos)
                self.screen.blit(station, station_rect)
            label = self.font.render(zone.name, True, (255, 255, 255))
            label_y = pos[1] + (ZONE_RADIUS if hub_image is None else 32) + 4
            self.screen.blit(label, (pos[0] - label.get_width() // 2, label_y))

        drone_colors = [
            (0, 255, 255), (255, 0, 255), (255, 255, 0),
            (0, 255, 0), (0, 120, 255), (255, 80, 80),
        ]
        for drone_id, zone in positions.items():
            pos = self.positions[zone.name]
            sprite_rect = self.drone_image.get_rect(center=pos)
            self.screen.blit(self.drone_image, sprite_rect)
            label = self.font.render(f"D{drone_id}", True, (255, 255, 255))
            self.screen.blit(label, (pos[0] + 12, pos[1] - 8))

        pygame.display.flip()

    def run(self) -> None:
        """Replays the simulation while keeping the window responsive."""
        running = True
        frame_index = 0
        elapsed = 0
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            if self.position_history:
                self._draw_frame(self.position_history[frame_index])
                elapsed += clock.tick(60)
                if elapsed >= 500 and frame_index < len(self.position_history) - 1:
                    frame_index += 1
                    elapsed = 0
            else:
                clock.tick(60)
        pygame.quit()