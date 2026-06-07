import pygame
import random
import settings
import os

class UFO:
    def __init__(self):
        self.width = 48
        self.height = 24
        self.y = 40
        self.speed = 150
        self.is_active = False
        self.x = 0
        self.direction = 1
        
        self.spawn_timer = random.uniform(10, 20)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Load sprite
        try:
            image = pygame.image.load(os.path.join("assets", "ufo.png")).convert_alpha()
            self.image = pygame.transform.scale(image, (self.width, self.height))
        except:
            self.image = None
            
    def update(self, delta_time):
        if not self.is_active:
            self.spawn_timer -= delta_time
            if self.spawn_timer <= 0:
                self.spawn()
            return
            
        self.x += self.speed * self.direction * delta_time
        self.rect.x = self.x
        
        # Check off-screen
        if (self.direction == 1 and self.x > settings.SCREEN_WIDTH) or \
           (self.direction == -1 and self.x + self.width < 0):
            self.despawn()
            
    def spawn(self):
        self.is_active = True
        self.direction = random.choice([1, -1])
        if self.direction == 1:
            self.x = -self.width
        else:
            self.x = settings.SCREEN_WIDTH
        self.rect.x = self.x
        
    def despawn(self):
        self.is_active = False
        self.spawn_timer = random.uniform(15, 30)
        
    def get_points(self):
        return random.choice([50, 100, 150, 300])
        
    def draw(self, surface):
        if self.is_active:
            if self.image:
                surface.blit(self.image, (self.x, self.y))
            else:
                pygame.draw.rect(surface, settings.COLORS["RED"], self.rect)
