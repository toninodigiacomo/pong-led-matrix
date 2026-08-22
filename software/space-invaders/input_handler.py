"""
Abstraction des entrées de jeu.

Aujourd'hui : clavier (pas encore de pad DIY assemblé).
Plus tard   : pad ESP32-S3 reconnu comme joystick USB (HID Gamepad),
              lu via pygame.joystick au lieu du clavier.

Le reste du code de jeu n'utilise QUE les méthodes de InputHandler
(move_axis, fire_pressed, pause_pressed...) - jamais directement le
clavier ou le joystick. Ça permet de basculer d'une source à l'autre
sans toucher à la logique de jeu.
"""

import pygame


class InputHandler:
    def __init__(self):
        self.joystick = None
        self._init_joystick_if_available()

    def _init_joystick_if_available(self):
        """
        Détecte automatiquement un pad ESP32-S3 branché en USB.
        Si aucun pad n'est trouvé, on reste sur le clavier - pratique
        pour développer/tester avant d'avoir le matériel.
        """
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Pad détecté : {self.joystick.get_name()}")
        else:
            print("Aucun pad détecté - contrôle au clavier (flèches + espace + P)")

    def move_axis(self):
        """
        Retourne une valeur entre -1.0 (gauche) et 1.0 (droite).

        - Pad ESP32 : lit l'axe du potentiomètre (HID Gamepad axis)
        - Clavier   : flèches gauche/droite (tout ou rien, -1 / 0 / 1)
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
        """Bouton 2 sur le pad (tir) - Espace au clavier."""
        if self.joystick:
            return self.joystick.get_button(1)
        keys = pygame.key.get_pressed()
        return keys[pygame.K_SPACE]

    def pause_pressed_this_frame(self, events):
        """
        Bouton 1 sur le pad (Start/Select -> pause en jeu) - touche P
        au clavier. Détecté sur l'appui (edge), pas en continu, pour
        éviter de basculer pause/reprise plusieurs fois par frame.
        """
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                return True
            if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                return True
        return False
