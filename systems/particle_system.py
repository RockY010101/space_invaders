import pygame
import random
import settings

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-150, 150)
        self.vy = random.uniform(-150, 150)
        self.lifetime = random.uniform(0.3, 0.7)
        self.initial_lifetime = self.lifetime
        self.color = color
        self.size = random.uniform(2, 6)
        
    def update(self, delta_time):
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time
        self.lifetime -= delta_time
        
    def draw(self, surface):
        if self.lifetime > 0:
            alpha = int((self.lifetime / self.initial_lifetime) * 255)
            surf = pygame.Surface((int(self.size), int(self.size)), pygame.SRCALPHA)
            surf.fill((self.color[0], self.color[1], self.color[2], alpha))
            surface.blit(surf, (int(self.x), int(self.y)))

class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    def spawn_explosion(self, x, y, color, count=20):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))
            
    def update(self, delta_time):
        for p in self.particles:
            p.update(delta_time)
        self.particles = [p for p in self.particles if p.lifetime > 0]
        
    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)
