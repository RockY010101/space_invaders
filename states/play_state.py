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

    def handle_input(self):
        pass # InputManager reads Pygame internally during update

    def update(self, delta_time):
        self.input_manager.update()
        
        # Pause toggle
        if self.input_manager.is_just_pressed(pygame.K_p) or self.input_manager.is_just_pressed(pygame.K_ESCAPE):
            self.is_paused = not self.is_paused
            
        if self.is_paused:
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
            self.wave_clear_timer = 2.0 # 2 second pause

    def draw(self, surface):
        surface.fill(settings.COLORS["BACKGROUND"])
        self.player.draw(surface)
        self.enemy_grid.draw(surface)
        self.ufo.draw(surface)
        self.bullet_manager.draw(surface)
        self.particle_system.draw(surface)
        self.hud.draw(surface)
        
        if self.is_paused:
            text_surf = self.font_large.render("PAUSED", True, settings.COLORS["YELLOW"])
            surface.blit(text_surf, (settings.SCREEN_WIDTH/2 - text_surf.get_width()/2, settings.SCREEN_HEIGHT/2))
        elif self.wave_clear_timer > 0:
            text_surf = self.font_large.render("WAVE CLEAR!", True, settings.COLORS["CYAN"])
            surface.blit(text_surf, (settings.SCREEN_WIDTH/2 - text_surf.get_width()/2, settings.SCREEN_HEIGHT/2))
