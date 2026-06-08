import pygame

class InputManager:
    def __init__(self):
        # Seed with the CURRENT key state so any keys already held when this
        # InputManager is created are NOT treated as "just pressed" on the
        # first update(). This prevents held keys (e.g. SPACE to shoot) from
        # ghosting through into a new state (GameOver / Menu) and instantly
        # skipping it.
        pressed = pygame.key.get_pressed()
        self._tracked_keys = [
            pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d,
            pygame.K_SPACE, pygame.K_p, pygame.K_ESCAPE, pygame.K_RETURN,
        ]
        self.keys_held = {k: bool(pressed[k]) for k in self._tracked_keys}
        self._previous_keys_held = self.keys_held.copy()
        self.keys_pressed_this_frame = {}


    def update(self):
        self._previous_keys_held = self.keys_held.copy()

        pressed = pygame.key.get_pressed()
        self.keys_held = {k: bool(pressed[k]) for k in self._tracked_keys}

        self.keys_pressed_this_frame = {
            k: self.keys_held[k] and not self._previous_keys_held.get(k, False)
            for k in self._tracked_keys
        }


    def is_held(self, key):
        return self.keys_held.get(key, False)

    def is_just_pressed(self, key):
        return self.keys_pressed_this_frame.get(key, False)
