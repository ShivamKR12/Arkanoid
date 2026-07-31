import pygame
import sys
import os
import math
import random
import asyncio

from game_objects import Paddle, Ball, Brick, PowerUp
from levels import load_level
from ui import show_start_screen, show_level_message, draw_top_bar, show_end_screen

class Game:
    def __init__(self):
        pygame.mixer.pre_init()
        pygame.init()

        # --- Constants ---
        self.SCREEN_WIDTH = 600
        self.SCREEN_HEIGHT = 700
        self.UI_HEIGHT = 50
        self.PADDLE_HEIGHT = 10
        self.BALL_RADIUS = 8
        self.BRICK_COLS = 10
        self.BRICK_WIDTH = self.SCREEN_WIDTH // self.BRICK_COLS
        self.BRICK_HEIGHT = 30
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        # --- Game State ---
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Arkanoid")
        self.clock = pygame.time.Clock()
        self.state = "START" # START, PLAYING, LEVEL_TRANSITION, GAME_OVER
        self.game_mode = 'easy'
        self.score = 0
        self.lives = 3
        self.current_level = 1
        self.final_win = False

        # --- Game Objects ---
        self.paddle = None
        self.balls = []
        self.bricks = []
        self.powerups = []

        # --- Assets ---
        self.sounds = self._load_sounds()

    def _load_sounds(self):
        return {
            'brick_hit': pygame.mixer.Sound(os.path.join('assets', 'sounds', 'brick_hit.ogg')),
            'unbreakable_hit': pygame.mixer.Sound(os.path.join('assets', 'sounds', 'unbreakable_hit.ogg')),
            'gun_shot': pygame.mixer.Sound(os.path.join('assets', 'sounds', 'gun_shot.ogg')),
            'collect_powerup': pygame.mixer.Sound(os.path.join('assets', 'sounds', 'collect_powerup.ogg')),
        }

    def _setup_level(self, level_num):
        # --- Reset game objects for the level ---
        self.bricks = load_level(f"level{level_num}.json", self.BRICK_WIDTH, self.BRICK_HEIGHT, self.UI_HEIGHT)
        self.powerups.clear()
        self.balls.clear()

        # --- Configure paddle and ball based on difficulty ---
        paddle_width = 100 if self.game_mode == 'hard' else 150
        self.ball_speed = 7 if self.game_mode == 'hard' else 5

        self.paddle = Paddle(
            self.SCREEN_WIDTH // 2 - paddle_width // 2,
            self.SCREEN_HEIGHT - 40,
            paddle_width, self.PADDLE_HEIGHT, self.SCREEN_WIDTH
        )
        self.reset_ball()

    def reset_ball(self):
        self.balls.clear()
        ball = Ball(
            self.paddle.rect.centerx,
            self.paddle.rect.top - self.BALL_RADIUS,
            self.BALL_RADIUS, self.ball_speed
        )
        self.balls.append(ball)

    def reset_after_life_lost(self):
        self.lives -= 1
        if self.lives > 0:
            self.paddle.reset()
            self.reset_ball()
        else:
            self.state = "GAME_OVER"
            self.final_win = False

    async def run(self):
        running = True
        while running:
            if self.state == "START":
                self.game_mode = await show_start_screen(self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
                self.current_level = 1
                self.score = 0
                self.lives = 3
                self.state = "LEVEL_TRANSITION"

            elif self.state == "LEVEL_TRANSITION":
                self._setup_level(self.current_level)
                await show_level_message(self.screen, self.current_level, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
                self.state = "PLAYING"

            elif self.state == "PLAYING":
                self.handle_events()
                self.update()
                self.draw()

            elif self.state == "GAME_OVER":
                show_end_screen(self.screen, self.final_win, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
                self.state = "START" # Return to start screen

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            await asyncio.sleep(0)

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.paddle.shoot():
                        self.sounds['gun_shot'].play()

    def update(self):
        keys = pygame.key.get_pressed()
        self.paddle.move(keys)
        self.paddle.update()

        # --- Update Powerups ---
        for powerup in self.powerups[:]:
            powerup.move()
            if powerup.rect.colliderect(self.paddle.rect):
                self.activate_powerup(powerup.type)
                self.powerups.remove(powerup)
            elif powerup.rect.top > self.SCREEN_HEIGHT:
                self.powerups.remove(powerup)

        # --- Update Bullets ---
        destroyed_bricks_by_bullet = self.paddle.update_bullets(self.bricks)
        if destroyed_bricks_by_bullet:
            self.sounds['brick_hit'].play()
            self.score += 10 * len(destroyed_bricks_by_bullet)

        # --- Update Balls ---
        for ball in self.balls[:]:
            prev_rect = ball.rect.copy()
            ball.move()

            # Wall collisions
            if ball.rect.left <= 0:
                ball.rect.left = 0
                ball.speed_x *= -1
            if ball.rect.right >= self.SCREEN_WIDTH:
                ball.rect.right = self.SCREEN_WIDTH
                ball.speed_x *= -1
            if ball.rect.top <= self.UI_HEIGHT:
                ball.rect.top = self.UI_HEIGHT
                ball.speed_y *= -1

            # Paddle collision
            if ball.rect.colliderect(self.paddle.rect) and prev_rect.bottom <= self.paddle.rect.top:
                self.paddle.handle_ball_collision(ball)

            # Brick collisions
            hit_brick = self.handle_brick_collision(ball, prev_rect)
            if hit_brick:
                self.score += 10

            # Out of bounds
            if ball.rect.top > self.SCREEN_HEIGHT:
                self.balls.remove(ball)

        if not self.balls:
            self.reset_after_life_lost()

        # --- Check for level clear ---
        if not any(b.brick_type != 'unbreakable' for b in self.bricks):
            self.current_level += 1
            next_level_path = os.path.join("levels", f"level{self.current_level}.json")
            if os.path.exists(next_level_path):
                self.state = "LEVEL_TRANSITION"
            else:
                self.final_win = True
                self.state = "GAME_OVER"

    def handle_brick_collision(self, ball, prev_ball_rect):
        hit_index = ball.rect.collidelist([b.rect for b in self.bricks])
        if hit_index == -1:
            return None

        brick = self.bricks[hit_index]
        ball.handle_collision(brick.rect, prev_ball_rect)

        if brick.brick_type == 'unbreakable':
            self.sounds['unbreakable_hit'].play()
        else:
            self.sounds['brick_hit'].play()
            destroyed = brick.hit()
            if destroyed:
                if random.random() < 0.3: # 30% chance to drop powerup
                    power_type = random.choice(['expand', 'life', 'multiball', 'gun'])
                    self.powerups.append(PowerUp(brick.rect.centerx, brick.rect.y, power_type))
                del self.bricks[hit_index]

        return brick

    def activate_powerup(self, power_type):
        self.sounds['collect_powerup'].play()
        if power_type == 'life' and self.lives < 5:
            self.lives += 1
        elif power_type == 'expand':
            self.paddle.activate_expand()
        elif power_type == 'gun':
            self.paddle.activate_gun()
        elif power_type == 'multiball':
            new_balls_count = random.choice([1, 2])
            for _ in range(new_balls_count):
                angle_rad = math.radians(random.uniform(-45, 45))
                new_ball = Ball(
                    self.paddle.rect.centerx,
                    self.paddle.rect.top - self.BALL_RADIUS,
                    self.BALL_RADIUS,
                    self.ball_speed
                )
                new_ball.speed_x = self.ball_speed * math.sin(angle_rad)
                new_ball.speed_y = -self.ball_speed * math.cos(angle_rad)
                self.balls.append(new_ball)

    def draw(self):
        self.screen.fill(self.BLACK)

        # Draw game objects
        self.paddle.draw(self.screen)
        for ball in self.balls:
            ball.draw(self.screen)
        for brick in self.bricks:
            brick.draw(self.screen)
        for powerup in self.powerups:
            powerup.draw(self.screen)

        # Draw UI
        draw_top_bar(self.screen, self.score, self.lives, self.SCREEN_WIDTH, self.UI_HEIGHT)

        # Draw gun timer bar
        if self.paddle.gun_active:
            self.paddle.draw_gun_timer(self.screen, self.SCREEN_WIDTH, self.UI_HEIGHT)

        pygame.display.flip()
        self.clock.tick(60)