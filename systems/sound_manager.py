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

        # --- Volume state ---
        # master_volume controls: explosion, ufo (environment sounds)
        # shoot_volume  controls: shoot sound only
        self.master_volume = 0.5
        self.shoot_volume  = 0.3
        self.master_muted  = False
        self.shoot_muted   = False

        self.sounds = {}

        self._load_sound("shoot",     "shoot.wav")
        self._load_sound("explosion", "explosion.wav")
        self._load_sound("ufo",       "ufo.wav")

        # Apply initial volumes
        self._apply_volumes()

    # ------------------------------------------------------------------ #
    #  Internal helpers                                                     #
    # ------------------------------------------------------------------ #

    def _load_sound(self, name, filename):
        path = os.path.join("assets", filename)
        if os.path.exists(path):
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
            except:
                self.sounds[name] = None
        else:
            self.sounds[name] = None

    def _apply_volumes(self):
        """Push current volume state to every loaded Sound object."""
        shoot_vol = 0.0 if self.shoot_muted else self.shoot_volume
        env_vol   = 0.0 if self.master_muted else self.master_volume

        if self.sounds.get("shoot"):
            self.sounds["shoot"].set_volume(shoot_vol)
        for name in ("explosion", "ufo"):
            if self.sounds.get(name):
                self.sounds[name].set_volume(env_vol)

    # ------------------------------------------------------------------ #
    #  Public volume controls (called from pause menu)                     #
    # ------------------------------------------------------------------ #

    def set_master_volume(self, value):
        """Set master (environment) volume 0.0 – 1.0 and apply immediately."""
        self.master_volume = max(0.0, min(1.0, value))
        self._apply_volumes()

    def set_shoot_volume(self, value):
        """Set shoot-sound volume 0.0 – 1.0 and apply immediately."""
        self.shoot_volume = max(0.0, min(1.0, value))
        self._apply_volumes()

    def toggle_master_mute(self):
        self.master_muted = not self.master_muted
        self._apply_volumes()

    def toggle_shoot_mute(self):
        self.shoot_muted = not self.shoot_muted
        self._apply_volumes()

    # ------------------------------------------------------------------ #
    #  Playback                                                            #
    # ------------------------------------------------------------------ #

    def play_shoot(self):
        """Play the shoot sound on a dedicated channel with a throttle.
        The sound fires at most once every 300 ms so rapid fire doesn't
        produce an ear-fatiguing barrage of identical sounds.
        """
        sound = self.sounds.get("shoot")
        if not sound or not self.shoot_channel or self.shoot_muted:
            return

        now = pygame.time.get_ticks()
        if now - self._last_shoot_sound_tick >= self._shoot_sound_interval:
            self._last_shoot_sound_tick = now
            self.shoot_channel.stop()
            self.shoot_channel.play(sound)

    def play(self, name):
        """Play an environment sound (explosion, ufo) if not muted."""
        if self.master_muted:
            return
        if name in self.sounds and self.sounds[name]:
            self.sounds[name].play()
