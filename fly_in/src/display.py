import sys
try:
    import pygame
except ModuleNotFoundError:
    print("Error")
    sys.exit()
from .models import DroneMap

WINDOW_SIZE = (1920, 1070)
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
    """Renders the static drone network (zones + connections)."""

    def __init__(self, drone_map: DroneMap) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Fly-in — Map Preview")
        self.font = pygame.font.SysFont("consolas", 14)
        self.drone_map = drone_map
        self._compute_layout()

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

    def draw_static_map(self) -> None:
        """Draws zones and connections once, then waits until the window is closed."""
        self.screen.fill((20, 20, 20))

        for conn in self.drone_map.connections:
            p1 = self.positions[conn.zone_a.name]
            p2 = self.positions[conn.zone_b.name]
            pygame.draw.line(self.screen, (100, 100, 100), p1, p2, 2)

        for zone in self.drone_map.zones.values():
            pos = self.positions[zone.name]
            color = COLORS.get(zone.color, COLORS[None])
            pygame.draw.circle(self.screen, color, pos, ZONE_RADIUS)
            label = self.font.render(zone.name, True, (255, 255, 255))
            self.screen.blit(label, (pos[0] - label.get_width() // 2, pos[1] + ZONE_RADIUS + 4))

        pygame.display.flip()

    def run(self) -> None:
        """Keeps the window open until the user closes it."""
        self.draw_static_map()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
        pygame.quit()