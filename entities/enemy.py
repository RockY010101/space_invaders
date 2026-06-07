import pygame
import settings
import os

class Enemy:
    def __init__(self, row, col, x, y, enemy_type):
        self.row = row
        self.col = col
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.enemy_type = enemy_type
        self.is_alive = True
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # We don't have sprites, use colors. 
        if self.enemy_type == 1:
            self.color = settings.COLORS["WHITE"]
            self.points = 10
        elif self.enemy_type == 2:
            self.color = settings.COLORS["GREEN"]
            self.points = 20
        else:
            self.color = settings.COLORS["YELLOW"]
            self.points = 30
            
        # Load sprite
        try:
            if self.enemy_type == 1:
                image = pygame.image.load(os.path.join("assets", "enemy_1.png")).convert_alpha()
            else:
                image = pygame.image.load(os.path.join("assets", "enemy_2.png")).convert_alpha()
            self.image = pygame.transform.scale(image, (self.width, self.height))
        except:
            self.image = None
            
    def update_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        
    def draw(self, surface):
        if self.is_alive:
            if self.image:
                surface.blit(self.image, (self.x, self.y))
            else:
                pygame.draw.rect(surface, self.color, self.rect)
