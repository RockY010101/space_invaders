import pygame
import settings

class Bullet:
    def __init__(self, x, y, velocity_y, owner_tag):
        self.width = 4
        self.height = 12
        self.x = x - self.width / 2
        self.y = y
        self.velocity_y = velocity_y
        self.owner_tag = owner_tag
        self.is_active = True
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Color based on owner
        if self.owner_tag == "player":
            self.color = settings.COLORS["CYAN"]
        else:
            self.color = settings.COLORS["RED"]

    def update(self, delta_time):
        if not self.is_active:
            return
            
        self.y += self.velocity_y * delta_time
        self.rect.y = self.y
        
        # Check off-screen
        if self.y < -self.height or self.y > settings.SCREEN_HEIGHT:
            self.is_active = False

    def draw(self, surface):
        if self.is_active:
            pygame.draw.rect(surface, self.color, self.rect)
