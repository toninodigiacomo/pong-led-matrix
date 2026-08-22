"""
# ╭────────────────────────────────────────────────────────────────────────────────────────────
# │   Entry point.
# ├────────────────────────────────────────────────────────────────────────────────────────────
# │   Today.   : directly launches Space Invaders in HDMI output
# │              (HDMI window), keyboard or gamepad if already connected.
# │   Later on : this file will become the Pong/Space Invaders selection menu,
# │              and `Display` will switch to the LED matrix. The rest of the code 
# │              (`space_invaders.py`,`input_handler.py`) will not need to be changed
# ├────────────────────────────────────────────────────────────────────────────────────────────
# │   The game loop is in `main()`, which calls the `update()` and `draw()` methods of
# │   `SpaceInvadersGame` (in `space_invaders.py`) every frame
# └────────────────────────────────────────────────────────────────────────────────────────────
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
