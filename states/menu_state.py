import pygame
import settings
import utils
from systems.input_manager import InputManager

class MenuState:
    def __init__(self, switch_state_callback):
        self.switch_state = switch_state_callback
        self.font_title = pygame.font.SysFont("Courier", 40, bold=True)
        self.font_normal = pygame.font.SysFont("Courier", 20, bold=True)
        self.high_score = utils.load_high_score()
        self.input_manager = InputManager()
        
    def handle_input(self):
        pass
            
    def update(self, delta_time):
        self.input_manager.update()
        if self.input_manager.is_just_pressed(pygame.K_SPACE):
            self.switch_state("PLAY")
        
    def draw(self, surface):
        surface.fill(settings.COLORS["BACKGROUND"])
        
        # Title
        title_surf = self.font_title.render("SPACE INVADERS", True, settings.COLORS["CYAN"])
        surface.blit(title_surf, (settings.SCREEN_WIDTH/2 - title_surf.get_width()/2, 200))
        
        # Prompt
        prompt_surf = self.font_normal.render("Press SPACE to Start", True, settings.COLORS["WHITE"])
        surface.blit(prompt_surf, (settings.SCREEN_WIDTH/2 - prompt_surf.get_width()/2, 400))
        
        # High score
        hs_surf = self.font_normal.render(f"High Score: {self.high_score}", True, settings.COLORS["YELLOW"])
        surface.blit(hs_surf, (settings.SCREEN_WIDTH/2 - hs_surf.get_width()/2, 500))
