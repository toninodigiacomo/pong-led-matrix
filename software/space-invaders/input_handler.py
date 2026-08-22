"""
# ╭────────────────────────────────────────────────────────────────────────────────────────────
# │   Abstraction of game inputs.
# ├────────────────────────────────────────────────────────────────────────────────────────────
# │   Today : keyboard (no DIY pad assembled yet).
# │   Later : ESP32-S3 pad recognized as a USB joystick (HID Gamepad),
# │           read via pygame.joystick instead of the keyboard.
# ├────────────────────────────────────────────────────────────────────────────────────────────
# │   The rest of the game code only uses the methods of InputHandler
# │   (move_axis, fire_pressed, pause_pressed...) - never directly the
# │   keyboard or the joystick. This allows switching between sources
# │   without touching the game logic.
# └────────────────────────────────────────────────────────────────────────────────────────────
"""

import pygame

class InputHandler:
    def __init__(self):
        self.joystick = None
        self._init_joystick_if_available()

    def _init_joystick_if_available(self):
        """
        Automatically detects an ESP32-S3 pad connected via USB.
        If no pad is found, it defaults to the keyboard—which is handy
        for developing and testing before you have the hardware.
        """
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Pad detected : {self.joystick.get_name()}")
        else:
            print("No pad detected - using keyboard (arrows + space + P)")

    def move_axis(self):
        """
        Returns a value between -1.0 (left) and 1.0 (right).

        - ESP32 Pad: reads the potentiometer axis (HID Gamepad axis)
        - Keyboard: left/right arrow keys (on/off, -1 / 0 / 1)
        """
        if self.joystick:
            axis = self.joystick.get_axis(0)  # axe horizontal du gamepad
            # petite zone morte pour éviter le bruit autour du centre
            return 0.0 if abs(axis) < 0.08 else axis

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            return -1.0
        if keys[pygame.K_RIGHT]:
            return 1.0
        return 0.0

    def fire_pressed(self):
        """Button 2 on the gamepad (shoot) - Space bar on the keyboard."""
        if self.joystick:
            return self.joystick.get_button(1)
        keys = pygame.key.get_pressed()
        return keys[pygame.K_SPACE]

    def pause_pressed_this_frame(self, events):
        """
        Button 1 on the gamepad (Start/Select -> pause in game) - P key
        on the keyboard. Detected on the press (edge), not continuously, to
        avoid toggling pause/resume multiple times per frame.
        """
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                return True
            if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                return True
        return False
