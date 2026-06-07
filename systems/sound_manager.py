import pygame
import os

class SoundManager:
    def __init__(self):
        try:
            pygame.mixer.init()
        except:
            pass # In case there's no audio device
            
        self.sounds = {}
        
        self._load_sound("shoot", "shoot.wav")
        self._load_sound("explosion", "explosion.wav")
        self._load_sound("ufo", "ufo.wav")
        
    def _load_sound(self, name, filename):
        path = os.path.join("assets", filename)
        if os.path.exists(path):
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
                self.sounds[name].set_volume(0.3)
            except:
                self.sounds[name] = None
        else:
            self.sounds[name] = None
            
    def play(self, name):
        if name in self.sounds and self.sounds[name]:
            self.sounds[name].play()
