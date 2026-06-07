import pygame
import settings

class HUD:
    def __init__(self, score_manager):
        self.score_manager = score_manager
        # Pygame must be initialized before this is called
        self.font = pygame.font.SysFont("Courier", 20, bold=True)
        
    def draw(self, surface):
        # Draw Score and Level top left
        score_text = f"Lv: {self.score_manager.level}  Score: {self.score_manager.score}"
        score_surface = self.font.render(score_text, True, settings.COLORS["WHITE"])
        surface.blit(score_surface, (20, 20))
        
        # Draw Lives top right
        lives_text = f"🚀 x{self.score_manager.lives}"
        # Some fonts cannot render emoji, so fallback just in case
        try:
            lives_surface = self.font.render(lives_text, True, settings.COLORS["WHITE"])
        except pygame.error:
            lives_text = f"LIVES x{self.score_manager.lives}"
            lives_surface = self.font.render(lives_text, True, settings.COLORS["WHITE"])
            
        surface.blit(lives_surface, (settings.SCREEN_WIDTH - lives_surface.get_width() - 20, 20))
