import pygame
import os
import settings
import utils
from systems.input_manager import InputManager

_MUSIC_PATH   = os.path.join("assets", "menu_music.mp3")
_FADE_MS      = 1500          # fade-out duration when game starts (ms)
_ICON_RECT    = pygame.Rect(14, 14, 32, 32)   # top-left mute toggle button


class MenuState:
    def __init__(self, switch_state_callback):
        self.switch_state  = switch_state_callback
        self.font_title    = pygame.font.SysFont("Courier", 40, bold=True)
        self.font_normal   = pygame.font.SysFont("Courier", 20, bold=True)
        self.font_small    = pygame.font.SysFont("Courier", 13, bold=True)
        self.high_score    = utils.load_high_score()
        self.input_manager = InputManager()

        # Music state
        self.music_on = True
        self._start_music()

        # Mouse state (for mute-icon click detection)
        self._mouse_was_down = False

    # ------------------------------------------------------------------ #
    #  Music helpers                                                        #
    # ------------------------------------------------------------------ #

    def _start_music(self):
        """Load and loop the menu background music if the file exists."""
        if not os.path.exists(_MUSIC_PATH):
            self.music_on = False
            return
        try:
            pygame.mixer.music.load(_MUSIC_PATH)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)   # -1 = loop forever
        except Exception:
            self.music_on = False

    def stop_music(self, fade=False):
        """Stop (or fade out) the menu music. Called before switching state."""
        try:
            if fade:
                pygame.mixer.music.fadeout(_FADE_MS)
            else:
                pygame.mixer.music.stop()
        except Exception:
            pass

    def _toggle_music(self):
        self.music_on = not self.music_on
        try:
            if self.music_on:
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()
        except Exception:
            pass

    # ------------------------------------------------------------------ #
    #  State interface                                                      #
    # ------------------------------------------------------------------ #

    def handle_input(self):
        pass

    def update(self, delta_time):
        self.input_manager.update()

        # --- Keyboard: start game ---
        if self.input_manager.is_just_pressed(pygame.K_SPACE):
            self.stop_music(fade=True)
            self.switch_state("PLAY")
            return

        # --- Mouse: mute icon click ---
        mouse_down = pygame.mouse.get_pressed()[0]
        clicked    = self._mouse_was_down and not mouse_down
        if clicked and _ICON_RECT.collidepoint(pygame.mouse.get_pos()):
            self._toggle_music()
        self._mouse_was_down = mouse_down

    # ------------------------------------------------------------------ #
    #  Drawing                                                             #
    # ------------------------------------------------------------------ #

    def _draw_speaker_icon(self, surface, rect, active):
        """Draw a speaker icon. `active` = True → sound on, False → muted."""
        col = settings.COLORS["CYAN"] if active else (120, 120, 120)
        cx  = rect.left + rect.width  // 2
        cy  = rect.top  + rect.height // 2
        s   = rect.width // 2

        # Speaker body polygon
        body = [
            (rect.left,           cy - s // 3),
            (rect.left + s // 2,  cy - s // 3),
            (rect.left + s,       cy - s // 2),
            (rect.left + s,       cy + s // 2),
            (rect.left + s // 2,  cy + s // 3),
            (rect.left,           cy + s // 3),
        ]
        pygame.draw.polygon(surface, col, body)

        if active:
            # Sound waves
            wx = rect.left + s + 3
            pygame.draw.arc(surface, col,
                            pygame.Rect(wx,     cy - 8,  8,  16), -1.0, 1.0, 2)
            pygame.draw.arc(surface, col,
                            pygame.Rect(wx + 6, cy - 13, 11, 26), -1.0, 1.0, 2)
        else:
            # Red X
            x1, y1 = rect.left + s + 3, cy - s // 2
            x2, y2 = rect.right - 1,    cy + s // 2
            pygame.draw.line(surface, (220, 60, 60), (x1, y1), (x2, y2), 2)
            pygame.draw.line(surface, (220, 60, 60), (x1, y2), (x2, y1), 2)

        # Hover glow ring
        if _ICON_RECT.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(surface, settings.COLORS["WHITE"],
                             rect.inflate(4, 4), 1, border_radius=5)

    def draw(self, surface):
        surface.fill(settings.COLORS["BACKGROUND"])

        # --- Title ---
        title_surf = self.font_title.render("SPACE INVADERS", True,
                                            settings.COLORS["CYAN"])
        surface.blit(title_surf,
                     (settings.SCREEN_WIDTH  // 2 - title_surf.get_width()  // 2, 200))

        # --- Prompt ---
        prompt_surf = self.font_normal.render("Press SPACE to Start", True,
                                              settings.COLORS["WHITE"])
        surface.blit(prompt_surf,
                     (settings.SCREEN_WIDTH // 2 - prompt_surf.get_width() // 2, 400))

        # --- High Score ---
        hs_surf = self.font_normal.render(f"High Score: {self.high_score}", True,
                                          settings.COLORS["YELLOW"])
        surface.blit(hs_surf,
                     (settings.SCREEN_WIDTH // 2 - hs_surf.get_width() // 2, 500))

        # --- Music toggle icon (top-left) ---
        self._draw_speaker_icon(surface, _ICON_RECT, self.music_on)

        # Small label under the icon
        lbl = self.font_small.render("MUSIC", True, (120, 120, 140))
        surface.blit(lbl, (_ICON_RECT.left - 1,
                           _ICON_RECT.bottom + 3))
