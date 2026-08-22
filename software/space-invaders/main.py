"""
Point d'entrée. Aujourd'hui : lance directement Space Invaders en sortie
HDMI (fenêtre agrandie), clavier ou pad si déjà branché.

Plus tard : ce fichier deviendra le menu de sélection Pong / Space Invaders,
et Display basculera sur la matrice LED. Le reste du code (space_invaders.py,
input_handler.py) n'aura pas besoin de changer.
"""

import sys
import pygame

from display import Display
from input_handler import InputHandler
from sound import SoundBank
from space_invaders import SpaceInvadersGame

FPS = 60


def main():
    display = Display(fullscreen=False)
    input_handler = InputHandler()
    sound_bank = SoundBank()
    clock = pygame.time.Clock()

    game = SpaceInvadersGame(sound_bank)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            # relance une partie après game over (touche R ou bouton 2)
            if game.is_over() and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game = SpaceInvadersGame(sound_bank)

        game.update(dt, input_handler, events)

        canvas = display.get_canvas()
        game.draw(canvas)
        display.present()

    display.quit()
    sys.exit()


if __name__ == "__main__":
    main()
