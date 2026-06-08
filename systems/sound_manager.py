import pygame
import os

class SoundManager:
    def __init__(self):
        try:
            pygame.mixer.init()
            # Reserve channel 0 exclusively for the shoot sound so it never
            # competes with other sounds and can be stopped/restarted cleanly.
            pygame.mixer.set_reserved(1)
            self.shoot_channel = pygame.mixer.Channel(0)
        except:
            self.shoot_channel = None

        # Minimum milliseconds between shoot sound triggers (0.3s)
        self._shoot_sound_interval = 300
        self._last_shoot_sound_tick = 0

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

    def play_shoot(self):
        """Play the shoot sound on a dedicated channel with a throttle.
        The sound fires at most once every 300ms so rapid fire doesn't
        produce an ear-fatiguing barrage of identical sounds.
        """
        sound = self.sounds.get("shoot")
        if not sound or not self.shoot_channel:
            return

        now = pygame.time.get_ticks()
        if now - self._last_shoot_sound_tick >= self._shoot_sound_interval:
            self._last_shoot_sound_tick = now
            self.shoot_channel.stop()
            self.shoot_channel.play(sound)

    def play(self, name):
        if name in self.sounds and self.sounds[name]:
            self.sounds[name].play()
