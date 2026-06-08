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

class PlayState:
    def __init__(self, switch_state_callback):
        self.switch_state = switch_state_callback
        self.input_manager = InputManager()
        self.bullet_manager = BulletManager()
        self.score_manager = ScoreManager()
        self.particle_system = ParticleSystem()
        self.sound_manager = SoundManager()
        self.player = Player()
        self.enemy_grid = EnemyGrid()
        self.ufo = UFO()
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
        self.font_large = pygame.font.SysFont("Courier", 40, bold=True)
        self.font_normal = pygame.font.SysFont("Courier", 24, bold=True)

        # Pause menu button rects (centered, defined once)
        btn_w, btn_h = 220, 52
        cx = settings.SCREEN_WIDTH // 2
        self._btn_resume = pygame.Rect(cx - btn_w // 2, 360, btn_w, btn_h)
        self._btn_menu   = pygame.Rect(cx - btn_w // 2, 440, btn_w, btn_h)

        # Track previous mouse button state to detect single clicks
        self._mouse_was_down = False

    def handle_input(self):
        pass  # InputManager reads Pygame internally during update

    def _handle_pause_input(self):
        """Process mouse hover and click inside the pause menu."""
        mouse_pos = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed()[0]  # left button

        # Detect click on the frame the button is released (down -> up)
        clicked = self._mouse_was_down and not mouse_down
        self._mouse_was_down = mouse_down

        if clicked:
            if self._btn_resume.collidepoint(mouse_pos):
                self.is_paused = False
            elif self._btn_menu.collidepoint(mouse_pos):
                self.switch_state("MENU")

    def update(self, delta_time):
        self.input_manager.update()
        
        # Pause toggle via keyboard
        if self.input_manager.is_just_pressed(pygame.K_p) or self.input_manager.is_just_pressed(pygame.K_ESCAPE):
            self.is_paused = not self.is_paused
            self._mouse_was_down = False  # Reset so release doesn't phantom-click

        if self.is_paused:
            self._handle_pause_input()
            return
        
        # If in wave clear pause, just wait and update particles
        if self.wave_clear_timer > 0:
            self.wave_clear_timer -= delta_time
            self.particle_system.update(delta_time)
            if self.wave_clear_timer <= 0:
                self.score_manager.level += 1
                self.bullet_manager.bullets.clear()
                self.enemy_grid.reset(self.score_manager.level)
            return
            
        self.player.update(delta_time, self.input_manager, self.bullet_manager, self.sound_manager)
        self.enemy_grid.update(delta_time, self.bullet_manager)
        self.ufo.update(delta_time)
        self.bullet_manager.update(delta_time)
        self.particle_system.update(delta_time)
        
        is_game_over = self.collision_system.check_all()
        if is_game_over:
            self.switch_state("GAME_OVER", final_score=self.score_manager.score)
            return
            
        # Trigger wave clear
        if self.enemy_grid.alive_count == 0:
            self.wave_clear_timer = 2.0  # 2 second pause

    def _draw_pause_menu(self, surface):
        """Draw the semi-transparent pause overlay with interactive buttons."""
        mouse_pos = pygame.mouse.get_pos()

        # --- Dark overlay ---
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        surface.blit(overlay, (0, 0))

        # --- Panel ---
        panel_rect = pygame.Rect(
            settings.SCREEN_WIDTH // 2 - 150,
            280,
            300, 240
        )
        panel_surf = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        panel_surf.fill((20, 20, 50, 210))
        surface.blit(panel_surf, panel_rect.topleft)
        pygame.draw.rect(surface, settings.COLORS["CYAN"], panel_rect, 2, border_radius=8)

        # --- Title ---
        title_surf = self.font_large.render("PAUSED", True, settings.COLORS["YELLOW"])
        surface.blit(title_surf, (
            settings.SCREEN_WIDTH // 2 - title_surf.get_width() // 2,
            300
        ))

        # --- Buttons ---
        for btn_rect, label in [
            (self._btn_resume, "RESUME"),
            (self._btn_menu,   "MAIN MENU"),
        ]:
            hovered = btn_rect.collidepoint(mouse_pos)

            # Button fill
            btn_color = (0, 200, 160, 220) if hovered else (30, 30, 70, 220)
            btn_surf = pygame.Surface((btn_rect.width, btn_rect.height), pygame.SRCALPHA)
            btn_surf.fill(btn_color)
            surface.blit(btn_surf, btn_rect.topleft)

            # Button border -- brighter when hovered
            border_color = settings.COLORS["WHITE"] if hovered else settings.COLORS["CYAN"]
            pygame.draw.rect(surface, border_color, btn_rect, 2, border_radius=6)

            # Button label
            label_surf = self.font_normal.render(label, True, settings.COLORS["WHITE"])
            surface.blit(label_surf, (
                btn_rect.centerx - label_surf.get_width() // 2,
                btn_rect.centery - label_surf.get_height() // 2,
            ))

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
            text_surf = self.font_large.render("WAVE CLEAR!", True, settings.COLORS["CYAN"])
            surface.blit(text_surf, (settings.SCREEN_WIDTH/2 - text_surf.get_width()/2, settings.SCREEN_HEIGHT/2))
