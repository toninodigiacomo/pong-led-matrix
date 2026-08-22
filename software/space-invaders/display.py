"""
Abstraction d'affichage.

Toute la logique de jeu dessine sur un petit canvas logique (64x64 pixels,
la résolution finale de la matrice LED). Ce module se charge ensuite de
l'afficher :
  - Aujourd'hui : agrandi dans une fenêtre pygame classique (sortie HDMI)
  - Plus tard   : envoyé directement à la matrice LED via rpi-rgb-led-matrix

Pour basculer vers la matrice LED, il suffira de remplacer le contenu de
`present()` par l'appel à la lib rpi-rgb-led-matrix (SetImage / SwapOnVSync),
sans toucher au reste du code de jeu.
"""

import pygame

# Résolution logique = résolution finale de la matrice LED (2 dalles 64x32 empilées)
LOGICAL_WIDTH = 64
LOGICAL_HEIGHT = 64

# Facteur d'agrandissement pour l'affichage HDMI (fenêtre de test sur écran classique)
HDMI_SCALE = 10


class Display:
    def __init__(self, scale=HDMI_SCALE, fullscreen=False):
        pygame.init()
        pygame.display.set_caption("Arcade LED Matrix - Test HDMI")

        self.scale = scale
        window_size = (LOGICAL_WIDTH * scale, LOGICAL_HEIGHT * scale)

        flags = pygame.FULLSCREEN if fullscreen else 0
        self.window = pygame.display.set_mode(window_size, flags)

        # Le "vrai" canvas de jeu : 64x64 pixels, c'est LUI que la logique
        # de jeu doit utiliser pour dessiner (pas self.window directement)
        self.canvas = pygame.Surface((LOGICAL_WIDTH, LOGICAL_HEIGHT))

    def get_canvas(self):
        """Retourne la surface 64x64 sur laquelle dessiner le jeu."""
        return self.canvas

    def clear(self, color=(0, 0, 0)):
        self.canvas.fill(color)

    def present(self):
        """
        Affiche le canvas 64x64 à l'écran.

        HDMI (aujourd'hui) : on agrandit avec un scale "au plus proche"
        (pas de lissage) pour garder un rendu pixel-art net, comme sur
        une vraie matrice LED.

        Matrice LED (plus tard) : remplacer ce bloc par l'envoi du
        buffer de pixels à rpi-rgb-led-matrix.
        """
        scaled = pygame.transform.scale(
            self.canvas,
            (LOGICAL_WIDTH * self.scale, LOGICAL_HEIGHT * self.scale),
        )
        self.window.blit(scaled, (0, 0))
        pygame.display.flip()

    def quit(self):
        pygame.quit()
