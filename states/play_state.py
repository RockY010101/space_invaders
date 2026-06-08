import pygame
import settings
from systems.input_manager import InputManager
from systems.bullet_manager import BulletManager
from systems.score_manager import ScoreManager
from systems.collision_system import CollisionSystem
from systems.particle_system import ParticleSystem
from systems.sound_manager import SoundManager
from entities.player import Player
from entities.enemy_grid import EnemyGrid
from entities.ufo import UFO
from ui.hud import HUD

# ---------------------------------------------------------------------------
# Layout constants for the pause panel (all positions in screen pixels)
# ---------------------------------------------------------------------------
_PANEL_X      = 110          # left edge of panel
_PANEL_Y      = 230          # top edge of panel
_PANEL_W      = 380          # panel width
_PANEL_H      = 360          # panel height  (taller to fit two sliders)
_CX           = _PANEL_X + _PANEL_W // 2   # horizontal centre of panel

# Icon area (square drawn speaker/gun shape)
_ICON_SIZE    = 26
# Slider track dimensions
_TRACK_H      = 10
_TRACK_W      = 200
_KNOB_R       = 8            # knob radius

# Row Y positions (relative to screen)
_TITLE_Y      = _PANEL_Y + 18
_MASTER_ROW_Y = _PANEL_Y + 90   # centre-line of master-volume row
_SHOOT_ROW_Y  = _PANEL_Y + 150  # centre-line of shoot-volume row
_RESUME_Y     = _PANEL_Y + 220
_MENU_Y       = _PANEL_Y + 292

# Icon rects (left side of each row)
_ICON_MASTER_RECT = pygame.Rect(_PANEL_X + 18, _MASTER_ROW_Y - _ICON_SIZE // 2,
                                _ICON_SIZE, _ICON_SIZE)
_ICON_SHOOT_RECT  = pygame.Rect(_PANEL_X + 18, _SHOOT_ROW_Y - _ICON_SIZE // 2,
                                _ICON_SIZE, _ICON_SIZE)

# Slider track rects
_TRACK_MASTER_X   = _PANEL_X + 60
_TRACK_SHOOT_X    = _PANEL_X + 60
_TRACK_MASTER = pygame.Rect(_TRACK_MASTER_X, _MASTER_ROW_Y - _TRACK_H // 2,
                            _TRACK_W, _TRACK_H)
_TRACK_SHOOT  = pygame.Rect(_TRACK_SHOOT_X,  _SHOOT_ROW_Y  - _TRACK_H // 2,
                            _TRACK_W, _TRACK_H)

# Button rects
_BTN_W, _BTN_H = 220, 50
_BTN_RESUME = pygame.Rect(_CX - _BTN_W // 2, _RESUME_Y, _BTN_W, _BTN_H)
_BTN_MENU   = pygame.Rect(_CX - _BTN_W // 2, _MENU_Y,   _BTN_W, _BTN_H)


class PlayState:
    def __init__(self, switch_state_callback):
        self.switch_state   = switch_state_callback
        self.input_manager  = InputManager()
        self.bullet_manager = BulletManager()
        self.score_manager  = ScoreManager()
        self.particle_system = ParticleSystem()
        self.sound_manager  = SoundManager()
        # Stop any menu background music that may still be fading out
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
        self.player         = Player()
        self.enemy_grid     = EnemyGrid()
        self.ufo            = UFO()
        self.collision_system = CollisionSystem(
            self.bullet_manager,
            self.enemy_grid,
            self.player,
            self.score_manager,
            self.particle_system,
            self.ufo,
            self.sound_manager
        )
        self.hud = HUD(self.score_manager)

        self.wave_clear_timer = 0
        self.is_paused = False

        self.font_large  = pygame.font.SysFont("Courier", 38, bold=True)
        self.font_normal = pygame.font.SysFont("Courier", 22, bold=True)
        self.font_small  = pygame.font.SysFont("Courier", 15, bold=True)

        # Mouse state
        self._mouse_was_down   = False
        # Which slider is currently being dragged: None | "master" | "shoot"
        self._dragging_slider  = None

    # ------------------------------------------------------------------ #
    #  Input                                                               #
    # ------------------------------------------------------------------ #

    def handle_input(self):
        pass  # InputManager reads Pygame internally during update

    def _handle_pause_input(self):
        """Process all mouse interaction inside the pause menu."""
        mx, my   = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed()[0]
        clicked    = self._mouse_was_down and not mouse_down   # rising-edge

        # ---- Slider drag logic ----
        if mouse_down:
            # Start a drag if mouse pressed inside a track (or knob area)
            if self._dragging_slider is None:
                if _TRACK_MASTER.inflate(0, 20).collidepoint(mx, my):
                    self._dragging_slider = "master"
                elif _TRACK_SHOOT.inflate(0, 20).collidepoint(mx, my):
                    self._dragging_slider = "shoot"

            # Apply drag
            if self._dragging_slider == "master":
                ratio = (mx - _TRACK_MASTER.left) / _TRACK_MASTER.width
                self.sound_manager.set_master_volume(ratio)
            elif self._dragging_slider == "shoot":
                ratio = (mx - _TRACK_SHOOT.left) / _TRACK_SHOOT.width
                self.sound_manager.set_shoot_volume(ratio)
        else:
            self._dragging_slider = None   # release drag

        # ---- Single-click actions (buttons & mute icons) ----
        if clicked:
            if _BTN_RESUME.collidepoint(mx, my):
                self.is_paused = False
            elif _BTN_MENU.collidepoint(mx, my):
                self.switch_state("MENU")
            elif _ICON_MASTER_RECT.collidepoint(mx, my):
                self.sound_manager.toggle_master_mute()
            elif _ICON_SHOOT_RECT.collidepoint(mx, my):
                self.sound_manager.toggle_shoot_mute()

        self._mouse_was_down = mouse_down

    # ------------------------------------------------------------------ #
    #  Update                                                              #
    # ------------------------------------------------------------------ #

    def update(self, delta_time):
        self.input_manager.update()

        # Pause toggle via keyboard
        if (self.input_manager.is_just_pressed(pygame.K_p) or
                self.input_manager.is_just_pressed(pygame.K_ESCAPE)):
            self.is_paused = not self.is_paused
            self._mouse_was_down  = False   # prevent phantom clicks
            self._dragging_slider = None

        if self.is_paused:
            self._handle_pause_input()
            return

        # Wave-clear pause
        if self.wave_clear_timer > 0:
            self.wave_clear_timer -= delta_time
            self.particle_system.update(delta_time)
            if self.wave_clear_timer <= 0:
                self.score_manager.level += 1
                self.bullet_manager.bullets.clear()
                self.enemy_grid.reset(self.score_manager.level)
            return

        self.player.update(delta_time, self.input_manager,
                           self.bullet_manager, self.sound_manager)
        self.enemy_grid.update(delta_time, self.bullet_manager)
        self.ufo.update(delta_time)
        self.bullet_manager.update(delta_time)
        self.particle_system.update(delta_time)

        if self.collision_system.check_all():
            self.switch_state("GAME_OVER", final_score=self.score_manager.score)
            return

        if self.enemy_grid.alive_count == 0:
            self.wave_clear_timer = 2.0

    # ------------------------------------------------------------------ #
    #  Drawing helpers                                                     #
    # ------------------------------------------------------------------ #

    def _draw_speaker_icon(self, surface, rect, muted, color):
        """Draw a minimal speaker icon inside `rect`. If muted, show an X."""
        cx = rect.left + rect.width // 2
        cy = rect.top  + rect.height // 2
        s  = rect.width // 2   # half-size

        # Speaker body (trapezoid-like polygon)
        body = [
            (rect.left,           cy - s // 3),
            (rect.left + s // 2,  cy - s // 3),
            (rect.left + s,       cy - s // 2),
            (rect.left + s,       cy + s // 2),
            (rect.left + s // 2,  cy + s // 3),
            (rect.left,           cy + s // 3),
        ]
        pygame.draw.polygon(surface, color, body)

        if muted:
            # Red X over the right side
            x1, y1 = rect.left + s + 3, cy - s // 2
            x2, y2 = rect.right - 1,    cy + s // 2
            pygame.draw.line(surface, (220, 60, 60), (x1, y1), (x2, y2), 2)
            pygame.draw.line(surface, (220, 60, 60), (x1, y2), (x2, y1), 2)
        else:
            # Sound waves (two arcs)
            wave_x = rect.left + s + 4
            pygame.draw.arc(surface, color,
                            pygame.Rect(wave_x, cy - 8, 8, 16),
                            -1.0, 1.0, 2)
            pygame.draw.arc(surface, color,
                            pygame.Rect(wave_x + 6, cy - 13, 11, 26),
                            -1.0, 1.0, 2)

    def _draw_gun_icon(self, surface, rect, muted, color):
        """Draw a minimal gun/laser icon for the shoot channel."""
        cx = rect.centerx
        cy = rect.centery
        s  = rect.width // 2

        # Simple horizontal rectangle as barrel
        barrel = pygame.Rect(rect.left, cy - 4, rect.width - 6, 8)
        pygame.draw.rect(surface, color, barrel, border_radius=2)

        # Small block handle
        handle = pygame.Rect(rect.right - 10, cy + 4, 8, 8)
        pygame.draw.rect(surface, color, handle, border_radius=1)

        # Muted indicator: red X
        if muted:
            pygame.draw.line(surface, (220, 60, 60),
                             (rect.left, rect.top), (rect.right, rect.bottom), 2)
            pygame.draw.line(surface, (220, 60, 60),
                             (rect.left, rect.bottom), (rect.right, rect.top), 2)

    def _draw_volume_row(self, surface, label, icon_rect, track_rect,
                         volume, muted, icon_draw_fn, mouse_pos):
        """Render one complete volume row: label, icon, track, knob, pct."""
        icon_color = (180, 180, 180) if muted else settings.COLORS["CYAN"]

        # Row label (small, above the slider row)
        lbl_surf = self.font_small.render(label, True, (160, 160, 200))
        surface.blit(lbl_surf, (icon_rect.left, icon_rect.top - 18))

        # Icon (clickable)
        icon_draw_fn(surface, icon_rect, muted, icon_color)
        # Hover ring on icon
        if icon_rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, settings.COLORS["WHITE"], icon_rect, 1,
                             border_radius=4)

        # Track background
        pygame.draw.rect(surface, (50, 50, 80), track_rect, border_radius=5)

        # Filled portion
        fill_w = int(track_rect.width * volume)
        if fill_w > 0:
            fill_col = (80, 80, 80) if muted else (0, 200, 160)
            fill_rect = pygame.Rect(track_rect.left, track_rect.top,
                                    fill_w, track_rect.height)
            pygame.draw.rect(surface, fill_col, fill_rect, border_radius=5)

        # Knob
        knob_x = track_rect.left + int(track_rect.width * volume)
        knob_y = track_rect.centery
        knob_col = (130, 130, 130) if muted else settings.COLORS["WHITE"]
        pygame.draw.circle(surface, knob_col, (knob_x, knob_y), _KNOB_R)
        pygame.draw.circle(surface, settings.COLORS["CYAN"],
                           (knob_x, knob_y), _KNOB_R, 2)

        # Percentage text
        pct_text = f"{'--' if muted else int(volume * 100):>3}%"
        pct_surf = self.font_small.render(pct_text, True,
                                          (120, 120, 120) if muted else (200, 200, 200))
        surface.blit(pct_surf, (track_rect.right + 8,
                                track_rect.centery - pct_surf.get_height() // 2))

    def _draw_pause_menu(self, surface):
        """Draw the full semi-transparent pause overlay."""
        mouse_pos = pygame.mouse.get_pos()

        # --- Screen dim ---
        overlay = pygame.Surface(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        surface.blit(overlay, (0, 0))

        # --- Panel background ---
        panel_rect = pygame.Rect(_PANEL_X, _PANEL_Y, _PANEL_W, _PANEL_H)
        panel_surf = pygame.Surface((panel_rect.width, panel_rect.height),
                                    pygame.SRCALPHA)
        panel_surf.fill((15, 15, 45, 220))
        surface.blit(panel_surf, panel_rect.topleft)
        pygame.draw.rect(surface, settings.COLORS["CYAN"], panel_rect,
                         2, border_radius=10)

        # --- Title ---
        title_surf = self.font_large.render("PAUSED", True,
                                            settings.COLORS["YELLOW"])
        surface.blit(title_surf,
                     (_CX - title_surf.get_width() // 2, _TITLE_Y))

        # --- Divider ---
        pygame.draw.line(surface, (40, 40, 80),
                         (_PANEL_X + 20, _TITLE_Y + 52),
                         (_PANEL_X + _PANEL_W - 20, _TITLE_Y + 52), 1)

        # --- Master volume row ---
        self._draw_volume_row(
            surface,
            label      = "MASTER VOLUME",
            icon_rect  = _ICON_MASTER_RECT,
            track_rect = _TRACK_MASTER,
            volume     = self.sound_manager.master_volume,
            muted      = self.sound_manager.master_muted,
            icon_draw_fn = self._draw_speaker_icon,
            mouse_pos  = mouse_pos,
        )

        # --- Shoot volume row ---
        self._draw_volume_row(
            surface,
            label      = "SHOOT VOLUME",
            icon_rect  = _ICON_SHOOT_RECT,
            track_rect = _TRACK_SHOOT,
            volume     = self.sound_manager.shoot_volume,
            muted      = self.sound_manager.shoot_muted,
            icon_draw_fn = self._draw_gun_icon,
            mouse_pos  = mouse_pos,
        )

        # --- Buttons ---
        for btn_rect, label in [
            (_BTN_RESUME, "RESUME"),
            (_BTN_MENU,   "MAIN MENU"),
        ]:
            hovered   = btn_rect.collidepoint(mouse_pos)
            btn_color = (0, 200, 160, 220) if hovered else (30, 30, 70, 220)
            btn_surf  = pygame.Surface((btn_rect.width, btn_rect.height),
                                       pygame.SRCALPHA)
            btn_surf.fill(btn_color)
            surface.blit(btn_surf, btn_rect.topleft)

            border_col = settings.COLORS["WHITE"] if hovered else settings.COLORS["CYAN"]
            pygame.draw.rect(surface, border_col, btn_rect, 2, border_radius=6)

            lbl_surf = self.font_normal.render(label, True,
                                               settings.COLORS["WHITE"])
            surface.blit(lbl_surf, (
                btn_rect.centerx - lbl_surf.get_width()  // 2,
                btn_rect.centery - lbl_surf.get_height() // 2,
            ))

    # ------------------------------------------------------------------ #
    #  Main draw                                                           #
    # ------------------------------------------------------------------ #

    def draw(self, surface):
        surface.fill(settings.COLORS["BACKGROUND"])
        self.player.draw(surface)
        self.enemy_grid.draw(surface)
        self.ufo.draw(surface)
        self.bullet_manager.draw(surface)
        self.particle_system.draw(surface)
        self.hud.draw(surface)

        if self.is_paused:
            self._draw_pause_menu(surface)
        elif self.wave_clear_timer > 0:
            text_surf = self.font_large.render("WAVE CLEAR!", True,
                                               settings.COLORS["CYAN"])
            surface.blit(text_surf, (
                settings.SCREEN_WIDTH  // 2 - text_surf.get_width()  // 2,
                settings.SCREEN_HEIGHT // 2,
            ))
