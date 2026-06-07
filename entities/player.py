import pygame
import settings
import os

class Player:
    def __init__(self):
        self.width = 40
        self.height = 20
        self.x = settings.PLAYER_START_X - self.width / 2
        self.y = settings.PLAYER_Y
        self.speed = settings.PLAYER_SPEED
        self.is_alive = True
        
        self.death_timer = 0.0
        self.cooldown_timer = 0
        self.cooldown_duration = 0.1 # Rapid fire
        
        # We don't have sprites yet, use a rect
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Load sprite
        try:
            image = pygame.image.load(os.path.join("assets", "player.png")).convert_alpha()
            self.image = pygame.transform.scale(image, (self.width, self.height))
        except:
            self.image = None

    def on_hit(self):
        self.is_alive = False
        self.death_timer = settings.PLAYER_RESPAWN_TIME

    def update(self, delta_time, input_manager, bullet_manager, sound_manager):
        if not self.is_alive:
            self.death_timer -= delta_time
            if self.death_timer <= 0:
                self.is_alive = True
                self.x = settings.PLAYER_START_X - self.width / 2
            return

        current_speed = self.speed
        if input_manager.is_held(pygame.K_SPACE):
            current_speed = self.speed * 0.75

        if input_manager.is_held(pygame.K_LEFT) or input_manager.is_held(pygame.K_a):
            self.x -= current_speed * delta_time
        if input_manager.is_held(pygame.K_RIGHT) or input_manager.is_held(pygame.K_d):
            self.x += current_speed * delta_time

        # Clamp to screen edges
        if self.x < 0:
            self.x = 0
        if self.x > settings.SCREEN_WIDTH - self.width:
            self.x = settings.SCREEN_WIDTH - self.width

        self.rect.x = self.x

        # Shooting
        if self.cooldown_timer > 0:
            self.cooldown_timer -= delta_time

        if input_manager.is_held(pygame.K_SPACE) and self.cooldown_timer <= 0:
            spawn_x = self.x + self.width / 2
            spawn_y = self.y
            if bullet_manager.spawn_player_bullet(spawn_x, spawn_y):
                self.cooldown_timer = self.cooldown_duration
                if sound_manager:
                    sound_manager.play("shoot")

    def draw(self, surface):
        if self.is_alive:
            if self.image:
                surface.blit(self.image, (self.x, self.y))
            else:
                pygame.draw.rect(surface, settings.COLORS["GREEN"], self.rect)
