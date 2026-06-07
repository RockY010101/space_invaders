import pygame

class InputManager:
    def __init__(self):
        self.keys_held = {}
        self.keys_pressed_this_frame = {}
        self._previous_keys_held = {}

    def update(self):
        self._previous_keys_held = self.keys_held.copy()
        
        pressed = pygame.key.get_pressed()
        self.keys_held = {
            pygame.K_LEFT: pressed[pygame.K_LEFT],
            pygame.K_RIGHT: pressed[pygame.K_RIGHT],
            pygame.K_a: pressed[pygame.K_a],
            pygame.K_d: pressed[pygame.K_d],
            pygame.K_SPACE: pressed[pygame.K_SPACE],
            pygame.K_p: pressed[pygame.K_p],
            pygame.K_ESCAPE: pressed[pygame.K_ESCAPE],
            pygame.K_RETURN: pressed[pygame.K_RETURN]
        }

        self.keys_pressed_this_frame = {}
        for key, is_held in self.keys_held.items():
            self.keys_pressed_this_frame[key] = is_held and not self._previous_keys_held.get(key, False)

    def is_held(self, key):
        return self.keys_held.get(key, False)

    def is_just_pressed(self, key):
        return self.keys_pressed_this_frame.get(key, False)
