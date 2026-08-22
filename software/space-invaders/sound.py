"""
Sons rétro générés en direct (ondes carrées), sans aucun fichier audio
externe - dans l'esprit 8-bit de Space Invaders/Pong d'origine.

Si l'initialisation audio échoue (pas de haut-parleur branché sur le
Pi pendant les tests HDMI, par exemple), le jeu continue silencieusement
plutôt que de planter.
"""

import numpy as np
import pygame

SAMPLE_RATE = 44100


class SoundBank:
    def __init__(self):
        self.enabled = True
        try:
            pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2)
        except pygame.error:
            print("Pas de sortie audio disponible - le jeu continue sans son.")
            self.enabled = False
            return

        self.shoot = self._make_beep(880, 0.06)
        self.explosion = self._make_noise(0.2)
        self.invader_step = self._make_beep(120, 0.05)
        self.game_over = self._make_beep(110, 0.6)

    def _make_beep(self, freq, duration):
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
        wave = np.sign(np.sin(freq * t * 2 * np.pi))
        fade = np.linspace(1, 0, len(wave))  # évite un petit clic en fin de son
        audio = (wave * fade * 20000).astype(np.int16)
        stereo = np.column_stack([audio, audio])
        return pygame.sndarray.make_sound(np.ascontiguousarray(stereo))

    def _make_noise(self, duration):
        n = int(SAMPLE_RATE * duration)
        wave = np.random.uniform(-1, 1, n)
        fade = np.linspace(1, 0, n)
        audio = (wave * fade * 20000).astype(np.int16)
        stereo = np.column_stack([audio, audio])
        return pygame.sndarray.make_sound(np.ascontiguousarray(stereo))

    def play(self, sound_name):
        if not self.enabled:
            return
        sound = getattr(self, sound_name, None)
        if sound:
            sound.play()
