"""
# ╭────────────────────────────────────────────────────────────────────────────────────────────
# │   Display Abstraction.
# ├────────────────────────────────────────────────────────────────────────────────────────────
# │   All game logic is drawn on a small logical canvas (64x64 pixels,
# │   the final resolution of the LED matrix). This module then handles
# │   displaying it:
# │     - Currently: scaled up in a standard Pygame window (HDMI output)
# │     - Later: sent directly to the LED matrix via rpi-rgb-led-matrix
# ├────────────────────────────────────────────────────────────────────────────────────────────
# │   To switch to the LED matrix, simply replace the contents of
# │   `present()` with a call to the rpi-rgb-led-matrix library (SetImage / SwapOnVSync),
# │   without changing the rest of the game code.
# └────────────────────────────────────────────────────────────────────────────────────────────
"""

import pygame

# Logical resolution = final resolution of the LED matrix (two 64x32 panels stacked)
LOGICAL_WIDTH = 64
LOGICAL_HEIGHT = 64

# Scale factor for HDMI display (test window on standard screen)
HDMI_SCALE = 10

class Display:
    def __init__(self, scale=HDMI_SCALE, fullscreen=False):
        pygame.init()
        pygame.display.set_caption("Arcade LED Matrix - Test HDMI")

        self.scale = scale
        window_size = (LOGICAL_WIDTH * scale, LOGICAL_HEIGHT * scale)

        flags = pygame.FULLSCREEN if fullscreen else 0
        self.window = pygame.display.set_mode(window_size, flags)

        # The "real" game canvas : 64x64 pixels, this is what the game logic
        # should use for drawing (not self.window directly)
        self.canvas = pygame.Surface((LOGICAL_WIDTH, LOGICAL_HEIGHT))

    def get_canvas(self):
        """Returns the 64x64 surface on which to draw the game."""
        return self.canvas

    def clear(self, color=(0, 0, 0)):
        self.canvas.fill(color)

    def present(self):
        """
        Displays the 64x64 canvas on the screen.

        HDMI (today) : we scale it up with a "nearest neighbor" scale
        (no smoothing) to keep a sharp pixel-art look, like on a real LED matrix.

        LED Matrix (later) : replace this block with the transmission of the
        pixel buffer to rpi-rgb-led-matrix.
        """
        scaled = pygame.transform.scale(
            self.canvas,
            (LOGICAL_WIDTH * self.scale, LOGICAL_HEIGHT * self.scale),
        )
        self.window.blit(scaled, (0, 0))
        pygame.display.flip()

    def quit(self):
        pygame.quit()
