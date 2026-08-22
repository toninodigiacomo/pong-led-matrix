"""
# ╭────────────────────────────────────────────────────────────────────────────────────────────
# │   Space Invaders, designed for a 64x64-pixel canvas.
# ├────────────────────────────────────────────────────────────────────────────────────────────
# │   Controls (via InputHandler, keyboard, or gamepad):
# │     - move_axis()    : move the ship horizontally
# │     - fire_pressed() : fire (hold down = automatic rapid-fire)
# │     - pause          : button 1 / P key
# ├────────────────────────────────────────────────────────────────────────────────────────────
# │   The game does not use pygame.display or the keyboard directly: it
# │   draws on the canvas provided by Display and reads input via
# │   InputHandler. This will allow you to connect the LED matrix and the ESP32 gamepad
# │   later without modifying this file.
# └────────────────────────────────────────────────────────────────────────────────────────────
"""

import random
import pygame

WIDTH, HEIGHT = 64, 64

WHITE = (255, 255, 255)
GREEN = (60, 220, 90)
RED = (230, 60, 60)
YELLOW = (230, 210, 60)
GREY = (120, 120, 120)

PLAYER_WIDTH, PLAYER_HEIGHT = 5, 3
PLAYER_SPEED = 40                       # pixels/seconde
PLAYER_Y = HEIGHT - 6

BULLET_SPEED = 60
FIRE_COOLDOWN = 0.35                    # seconds between shots

INVADER_COLS = 8
INVADER_ROWS = 4
INVADER_W, INVADER_H = 5, 4
INVADER_SPACING_X = 7
INVADER_SPACING_Y = 6
INVADER_TOP = 6 
INVADER_STEP_DOWN = 3
INVADER_BULLET_SPEED = 30
INVADER_FIRE_CHANCE_PER_SEC = 0.6       # probability that an invader will fire, per second

class Player:
    def __init__(self):
        self.x = WIDTH / 2 - PLAYER_WIDTH / 2
        self.y = PLAYER_Y
        self.lives = 3

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), PLAYER_WIDTH, PLAYER_HEIGHT)

    def update(self, dt, axis):
        self.x += axis * PLAYER_SPEED * dt
        self.x = max(0, min(WIDTH - PLAYER_WIDTH, self.x))

    def draw(self, canvas):
        pygame.draw.rect(canvas, GREEN, self.rect())


class Bullet:
    def __init__(self, x, y, speed, color):
        self.x = x
        self.y = y
        self.speed = speed              # positive = down, negative = up
        self.color = color
        self.alive = True

    def update(self, dt):
        self.y += self.speed * dt
        if self.y < -2 or self.y > HEIGHT + 2:
            self.alive = False

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), 1, 3)

    def draw(self, canvas):
        pygame.draw.rect(canvas, self.color, self.rect())


class InvaderSwarm:
    def __init__(self):
        self.invaders = []
        for row in range(INVADER_ROWS):
            for col in range(INVADER_COLS):
                x = 4 + col * INVADER_SPACING_X
                y = INVADER_TOP + row * INVADER_SPACING_Y
                self.invaders.append([x, y, True])  # x, y, alive

        self.direction = 1              # 1 = right, -1 = left
        self.base_speed = 6             # pixels per second; it increases as the number remaining decreases
        self.move_timer = 0.0
        self.step_interval = 0.8        # seconds between 2 steps (way of the original game, jerky)

    def alive_count(self):
        return sum(1 for inv in self.invaders if inv[2])

    def update(self, dt, sound):
        alive = self.alive_count()
        if alive == 0:
            return

        # the rhythm accelerates as there are fewer invaders left
        self.step_interval = max(0.12, 0.15 + 0.65 * (alive / (INVADER_COLS * INVADER_ROWS)))

        self.move_timer += dt
        if self.move_timer < self.step_interval:
            return
        self.move_timer = 0.0

        # calculate if we hit an edge with this step
        min_x = min(inv[0] for inv in self.invaders if inv[2])
        max_x = max(inv[0] + INVADER_W for inv in self.invaders if inv[2])

        hit_edge = (max_x + self.direction * self.base_speed_step() >= WIDTH) or \
                   (min_x + self.direction * self.base_speed_step() <= 0)

        if hit_edge:
            self.direction *= -1
            for inv in self.invaders:
                inv[1] += INVADER_STEP_DOWN
        else:
            for inv in self.invaders:
                inv[0] += self.direction * self.base_speed_step()

        sound.play("invader_step")

    def base_speed_step(self):
        return 2                        # fixed step by "tick" of movement (way of the original game, jerky)

    def lowest_y(self):
        alive = [inv[1] + INVADER_H for inv in self.invaders if inv[2]]
        return max(alive) if alive else 0

    def maybe_fire(self, dt):
        """Return an enemy fire position, or None."""
        if random.random() < INVADER_FIRE_CHANCE_PER_SEC * dt:
            shooters = [inv for inv in self.invaders if inv[2]]
            if shooters:
                inv = random.choice(shooters)
                return inv[0] + INVADER_W / 2, inv[1] + INVADER_H
        return None

    def draw(self, canvas):
        for x, y, alive in self.invaders:
            if alive:
                pygame.draw.rect(canvas, WHITE, pygame.Rect(int(x), int(y), INVADER_W, INVADER_H))


class SpaceInvadersGame:
    """
    A Space Invaders game. Usage:
    game = SpaceInvadersGame(sound_bank)
    while running:
        game.update(dt, input_handler, events)
        game.draw(canvas)
        if game.is_over():
            ...
    """

    def __init__(self, sound_bank):
        self.sound = sound_bank
        self.player = Player()
        self.swarm = InvaderSwarm()
        self.player_bullets = []
        self.invader_bullets = []
        self.fire_cooldown_timer = 0.0
        self.score = 0
        self.game_over = False
        self.won = False
        self.paused = False

    def is_over(self):
        return self.game_over

    def update(self, dt, input_handler, events):
        if self.game_over:
            return

        if input_handler.pause_pressed_this_frame(events):
            self.paused = not self.paused
        if self.paused:
            return

        axis = input_handler.move_axis()
        self.player.update(dt, axis)

        # player shot
        self.fire_cooldown_timer -= dt
        if input_handler.fire_pressed() and self.fire_cooldown_timer <= 0:
            bx = self.player.x + PLAYER_WIDTH / 2
            self.player_bullets.append(Bullet(bx, self.player.y, -BULLET_SPEED, YELLOW))
            self.sound.play("shoot")
            self.fire_cooldown_timer = FIRE_COOLDOWN

        # invader shots
        self.swarm.update(dt, self.sound)
        fire_pos = self.swarm.maybe_fire(dt)
        if fire_pos:
            fx, fy = fire_pos
            self.invader_bullets.append(Bullet(fx, fy, INVADER_BULLET_SPEED, RED))

        # update shots
        for b in self.player_bullets:
            b.update(dt)
        for b in self.invader_bullets:
            b.update(dt)
        self.player_bullets = [b for b in self.player_bullets if b.alive]
        self.invader_bullets = [b for b in self.invader_bullets if b.alive]

        self._handle_collisions()

        #   game over : an invader reached the player or the player has no more lives
        if self.swarm.lowest_y() >= self.player.y or self.player.lives <= 0:
            self.game_over = True
            self.won = False
            self.sound.play("game_over")

        # victory : no more invaders
        if self.swarm.alive_count() == 0:
            self.game_over = True
            self.won = True

    def _handle_collisions(self):
        # player shots vs invaders
        for b in self.player_bullets:
            if not b.alive:
                continue
            for inv in self.swarm.invaders:
                if not inv[2]:
                    continue
                inv_rect = pygame.Rect(int(inv[0]), int(inv[1]), INVADER_W, INVADER_H)
                if inv_rect.colliderect(b.rect()):
                    inv[2] = False
                    b.alive = False
                    self.score += 10
                    self.sound.play("explosion")
                    break

        # invader shots vs player
        player_rect = self.player.rect()
        for b in self.invader_bullets:
            if b.alive and player_rect.colliderect(b.rect()):
                b.alive = False
                self.player.lives -= 1
                self.sound.play("explosion")

        self.player_bullets = [b for b in self.player_bullets if b.alive]
        self.invader_bullets = [b for b in self.invader_bullets if b.alive]

    def draw(self, canvas):
        canvas.fill((0, 0, 0))
        self.player.draw(canvas)
        self.swarm.draw(canvas)
        for b in self.player_bullets:
            b.draw(canvas)
        for b in self.invader_bullets:
            b.draw(canvas)

        # score at the top (very small font, pixel-based)
        self._draw_score(canvas)

        if self.paused:
            self._draw_text_center(canvas, "PAUSE", GREY, y=WIDTH // 2)

        if self.game_over:
            msg = "WIN" if self.won else "GAME OVER"
            self._draw_text_center(canvas, msg, YELLOW if self.won else RED, y=WIDTH // 2)

    def _draw_score(self, canvas):
        # health bar in the upper-left corner (small squares), score not displayed in
        # Numbers, kept simple at 64x64—to be improved with a font dedicated pixel 
        # later if needed
        for i in range(self.player.lives):
            pygame.draw.rect(canvas, GREEN, pygame.Rect(2 + i * 4, 1, 2, 2))

    def _draw_text_center(self, canvas, text, color, y):
        # Minimal text rendering using the default Pygame font, scaled down to the specified size
        #   of the canvas—enough for a short 64x64 message
        font = pygame.font.SysFont(None, 12)
        surf = font.render(text, False, color)
        rect = surf.get_rect(center=(WIDTH // 2, y))
        canvas.blit(surf, rect)
