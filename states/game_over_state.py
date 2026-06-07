import pygame
import settings
import utils
from systems.input_manager import InputManager

class GameOverState:
    def __init__(self, switch_state_callback, final_score):
        self.switch_state = switch_state_callback
        self.final_score = final_score
        
        self.font_title = pygame.font.SysFont("Courier", 40, bold=True)
        self.font_normal = pygame.font.SysFont("Courier", 20, bold=True)
        
        self.high_score = utils.load_high_score()
        self.is_new_highscore = False
        self.input_manager = InputManager()
        
        if self.final_score > self.high_score:
            self.high_score = self.final_score
            self.is_new_highscore = True
            utils.save_high_score(self.high_score)
            
    def handle_input(self):
        pass
            
    def update(self, delta_time):
        self.input_manager.update()
        if self.input_manager.is_just_pressed(pygame.K_SPACE):
            self.switch_state("MENU")
        
    def draw(self, surface):
        surface.fill(settings.COLORS["BACKGROUND"])
        
        # Title
        title_surf = self.font_title.render("GAME OVER", True, settings.COLORS["RED"])
        surface.blit(title_surf, (settings.SCREEN_WIDTH/2 - title_surf.get_width()/2, 200))
        
        # Score
        score_surf = self.font_normal.render(f"Final Score: {self.final_score}", True, settings.COLORS["WHITE"])
        surface.blit(score_surf, (settings.SCREEN_WIDTH/2 - score_surf.get_width()/2, 350))
        
        if self.is_new_highscore:
            hs_surf = self.font_normal.render("NEW HIGH SCORE!", True, settings.COLORS["YELLOW"])
            surface.blit(hs_surf, (settings.SCREEN_WIDTH/2 - hs_surf.get_width()/2, 400))
            
        # Prompt
        prompt_surf = self.font_normal.render("Press SPACE for Menu", True, settings.COLORS["CYAN"])
        surface.blit(prompt_surf, (settings.SCREEN_WIDTH/2 - prompt_surf.get_width()/2, 500))
