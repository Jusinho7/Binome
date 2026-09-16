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
    def __init__(
        self,
        drone_map: DroneMap,
        position_history: list[dict[int, Zone]],
        turn_log: list[list[str]] | None = None,
    ) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.background = pygame.transform.smoothscale(
            pygame.image.load(BACKGROUND_IMAGE).convert(),
            WINDOW_SIZE
        )
        drone_image = pygame.image.load(DRONE_IMAGE).convert_alpha()
        self.drone_image = pygame.transform.smoothscale(drone_image, (54, 36))
        self.station_image = None
        if os.path.exists(STATION_IMAGE):
            station_image = pygame.image.load(STATION_IMAGE).convert_alpha()
            self.station_image = pygame.transform.smoothscale(
                station_image, (46, 46)
            )
        self.start_image = self._load_hub_image(START_IMAGE)
        self.end_image = self._load_hub_image(END_IMAGE)
        pygame.display.set_caption("Fly-in — Map Preview")
        self.font = pygame.font.SysFont("consolas", 14)
        self.hud_font = pygame.font.SysFont("consolas", 16)
        self.drone_map = drone_map
        self.position_history = position_history
        self.turn_log = turn_log or []
        self.paused = False
        self.speed = 1.0
        self.help_visible = False
        hud_group_width = 460 + 12 + 100
        hud_group_x = (WINDOW_SIZE[0] - hud_group_width) // 2
        self.hud_rect = pygame.Rect(hud_group_x, 20, 460, 50)
        self.help_button_rect = pygame.Rect(self.hud_rect.right + 12, 20, 100, 44)
        self.help_panel_rect = pygame.Rect(self.help_button_rect.x, 72, 330, 260)
        self._compute_layout()

    def _load_hub_image(self, image_path: str) -> pygame.Surface | None:
        if not os.path.exists(image_path):
            return self.station_image
        image = pygame.image.load(image_path).convert_alpha()
        return pygame.transform.smoothscale(image, (46, 46))

    def _compute_layout(self) -> None:
        """Maps zone (x, y) coordinates to screen pixel positions."""
        xs = [z.x for z in self.drone_map.zones.values()]
        ys = [z.y for z in self.drone_map.zones.values()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        margin = 120
        span_x = (max_x - min_x) or 1
        span_y = (max_y - min_y) or 1
        scale = min(
            (WINDOW_SIZE[0] - 2 * margin) / span_x,
            (WINDOW_SIZE[1] - 2 * margin) / span_y,
        ) * 0.82
        graph_width = span_x * scale
        graph_height = span_y * scale
        offset_x = (WINDOW_SIZE[0] - graph_width) / 2
        offset_y = (WINDOW_SIZE[1] - graph_height) / 2

        self.positions: dict[str, tuple[int, int]] = {}
        for zone in self.drone_map.zones.values():
            px = offset_x + (zone.x - min_x) * scale
            py = offset_y + (zone.y - min_y) * scale
            self.positions[zone.name] = (int(px), int(py))

    def _draw_frame(
        self,
        positions: dict[int, Zone],
        next_positions: dict[int, Zone] | None = None,
        progress: float = 0.0,
        turn_number: int = 0,
    ) -> None:
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
            label_y = pos[1] + (ZONE_RADIUS if hub_image is None else 23) + 4
            self.screen.blit(label, (pos[0] - label.get_width() // 2, label_y))

        for drone_id, zone in positions.items():
            start_x, start_y = self.positions[zone.name]
            end_x, end_y = start_x, start_y
            if next_positions is not None and drone_id in next_positions:
                next_zone = next_positions[drone_id]
                end_x, end_y = self.positions[next_zone.name]
            pos = (
                round(start_x + (end_x - start_x) * progress),
                round(start_y + (end_y - start_y) * progress),
            )
            sprite_rect = self.drone_image.get_rect(center=pos)
            self.screen.blit(self.drone_image, sprite_rect)
            label = self.font.render(f"D{drone_id}", True, (255, 255, 255))
            self.screen.blit(label, (pos[0] + 12, pos[1] - 8))

        self._draw_hud(turn_number)
        self._draw_movement(turn_number)
        pygame.display.flip()

    def _draw_hud(self, turn_number: int = 0) -> None:
        status = "PAUSE" if self.paused else "LECTURE"
        status_color = (255, 210, 80) if self.paused else (130, 255, 150)
        lines = [
            f"{status}  |  Tour: {turn_number}/{max(len(self.position_history) - 1, 0)}  |  Vitesse: x{self.speed:g}"
        ]
        panel = pygame.Surface(self.hud_rect.size, pygame.SRCALPHA)
        panel.fill((0, 0, 0, 180))
        self.screen.blit(panel, self.hud_rect.topleft)
        for index, line in enumerate(lines):
            color = status_color if index == 0 else (240, 240, 240)
            text = self.hud_font.render(line, True, color)
            text_rect = text.get_rect(center=self.hud_rect.center)
            self.screen.blit(text, text_rect)

        mouse_over_help = self.help_button_rect.collidepoint(pygame.mouse.get_pos())
        button_color = (70, 130, 210) if mouse_over_help else (45, 85, 150)
        pygame.draw.rect(self.screen, button_color, self.help_button_rect, border_radius=6)
        pygame.draw.rect(self.screen, (220, 235, 255), self.help_button_rect, 2, border_radius=6)
        help_text = self.hud_font.render("HELP", True, (255, 255, 255))
        help_rect = help_text.get_rect(center=self.help_button_rect.center)
        self.screen.blit(help_text, help_rect)

        if self.help_visible:
            help_panel = pygame.Surface(self.help_panel_rect.size, pygame.SRCALPHA)
            help_panel.fill((0, 0, 0, 220))
            self.screen.blit(help_panel, self.help_panel_rect.topleft)
            pygame.draw.rect(self.screen, (220, 235, 255), self.help_panel_rect, 2, border_radius=6)

            help_lines = [
                    "COMMANDS",
                    "Space -> Pause / Resume",
                    "R -> Restart",
                    "+ / - -> Change speed",
                    "N -> Next turn",
                    "B -> Previous turn",
                    "0 -> Normal speed",
                    "Escape -> Quit",
                    "H -> Show / hide help",
            ]
            for index, line in enumerate(help_lines):
                color = (255, 220, 100) if index == 0 else (245, 245, 245)
                text = self.font.render(line, True, color)
                self.screen.blit(text, (self.help_panel_rect.x + 16, self.help_panel_rect.y + 12 + index * 26))

    def _draw_movement(self, turn_number: int) -> None:
        if turn_number == 0:
            movement = "Debut de la simulation"
        elif turn_number <= len(self.turn_log):
            moves = self.turn_log[turn_number - 1]
            movement = " ".join(moves) if moves else "(attente)"
        else:
            movement = "(aucun deplacement)"

        text = self.font.render(f"Tour {turn_number}: {movement}", True, (245, 245, 245))
        panel_width = min(max(text.get_width() + 32, 360), WINDOW_SIZE[0] - 80)
        panel = pygame.Surface((panel_width, 38), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 190))
        panel_x = (WINDOW_SIZE[0] - panel_width) // 2
        panel_y = WINDOW_SIZE[1] - 58
        self.screen.blit(panel, (panel_x, panel_y))
        text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, panel_y + 19))
        self.screen.blit(text, text_rect)

    def run(self) -> None:
        running = True
        frame_index = 0
        elapsed = 0.0
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.help_button_rect.collidepoint(event.pos):
                        self.help_visible = not self.help_visible
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key in (pygame.K_SPACE, pygame.K_p):
                        self.paused = not self.paused
                    elif event.key == pygame.K_r:
                        frame_index = 0
                        elapsed = 0
                        self.paused = False
                    elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                        self.speed = min(self.speed * 2, 8.0)
                    elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                        self.speed = max(self.speed / 2, 0.25)
                    elif event.key == pygame.K_0:
                        self.speed = 1.0
                    elif event.key == pygame.K_h:
                        self.help_visible = not self.help_visible
                    elif event.key == pygame.K_n:
                        frame_index = min(frame_index + 1, len(self.position_history) - 1)
                        elapsed = 0
                        self.paused = True
                    elif event.key == pygame.K_b:
                        frame_index = max(frame_index - 1, 0)
                        elapsed = 0
                        self.paused = True
                    elif event.key == pygame.K_RIGHT:
                        frame_index = min(frame_index + 1, len(self.position_history) - 1)
                        elapsed = 0
                        self.paused = True
                    elif event.key == pygame.K_LEFT:
                        frame_index = max(frame_index - 1, 0)
                        elapsed = 0
                        self.paused = True
                    elif event.key == pygame.K_HOME:
                        frame_index = 0
                        elapsed = 0
                        self.paused = True
                    elif event.key == pygame.K_END:
                        frame_index = len(self.position_history) - 1
                        elapsed = 0
                        self.paused = True

            if self.position_history:
                next_positions = None
                if frame_index < len(self.position_history) - 1:
                    next_positions = self.position_history[frame_index + 1]
                self._draw_frame(
                    self.position_history[frame_index],
                    next_positions,
                    min(elapsed / 500, 1.0),
                    frame_index,
                )
                delta_time = clock.tick(60)
                if not self.paused:
                    elapsed += delta_time * self.speed
                    if elapsed >= 500 and frame_index < len(self.position_history) - 1:
                        frame_index += 1
                        elapsed = 0
            else:
                clock.tick(60)
        pygame.quit()
