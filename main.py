import math
import random
import sys
import os
import pygame
import pygame.base
import asyncio

from Powerups import PowerUp
from levels import load_level
from bricks import Brick
from ui import show_start_screen, show_level_message, draw_top_bar, show_end_screen
from player import Paddle

pygame.mixer.pre_init()
pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arkanoid")

game_mode = show_start_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
show_level_message(screen, 1, SCREEN_WIDTH, SCREEN_HEIGHT)

original_paddle_width = 120 if game_mode == 'hard' else 200
ball_speed = 10 if game_mode == 'hard' else 5

current_level = 1
win = False
final_win = False
UI_HEIGHT = 50

#Sounds
sound_path = os.path.join('assets', 'sounds', 'brick_hit.ogg')
brick_sound = pygame.mixer.Sound(sound_path)
unbr_sound_path = os.path.join('assets', 'sounds', 'unbreakable_hit.ogg')
unbreakable_sound = pygame.mixer.Sound(unbr_sound_path)
gun_sound_path = os.path.join('assets', 'sounds', 'gun_shot.ogg')
gun_sound = pygame.mixer.Sound(gun_sound_path)
powerup_path = os.path.join('assets', 'sounds', 'collect_powerup.ogg')
powerup_sound = pygame.mixer.Sound(powerup_path)


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

paddle = Paddle(
    SCREEN_WIDTH // 2 - original_paddle_width // 2,
    SCREEN_HEIGHT - 40,
    original_paddle_width,
    10,  # paddle height
    SCREEN_WIDTH
)
# paddle_speed = 10

ball_radius = 8
balls = [{
    'rect': pygame.Rect(
        paddle.rect.centerx - ball_radius,
        paddle.rect.top - ball_radius * 2 - 2,
        ball_radius * 2,
        ball_radius * 2
    ),
    'speed_x': ball_speed,
    'speed_y': -ball_speed
}]

brick_cols = 10
brick_width = SCREEN_WIDTH // brick_cols
brick_height = 30
bricks = load_level(f"level{current_level}.json", brick_width, brick_height, UI_HEIGHT)

score = 0
lives = 3
expand_active = False
expand_end_time = 0
font = pygame.font.Font(None, 36)
hit_bricks = []
powerups = []

clock = pygame.time.Clock()
running = True

async def main():
    global running, win, final_win, lives, score, current_level
    global balls, bricks, powerups, expand_active, expand_end_time
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if paddle.shoot():
                        gun_sound.play()

        keys = pygame.key.get_pressed()
        paddle.move(keys)

        for ball in balls:
            ball['rect'].x += ball['speed_x']
            ball['rect'].y += ball['speed_y']

        for powerup in powerups[:]:
            powerup.move()
            if powerup.rect.colliderect(paddle):
                powerup_sound.play()
                if powerup.type == 'life' and lives < 5:
                    lives += 1
                elif powerup.type == 'expand':
                    paddle.activate_expand()

                    expand_active = True
                    expand_end_time = pygame.time.get_ticks() + 10000
                elif powerup.type == 'multiball':
                    new_balls = random.choice([1, 2])
                    for _ in range(new_balls):
                        angle_rad = math.radians(random.uniform(-45, 45))
                        balls.append({
                            'rect': pygame.Rect(paddle.rect.centerx, paddle.rect.top - 20, ball_radius * 2, ball_radius * 2),
                            'speed_x': ball_speed * math.sin(angle_rad),
                            'speed_y': -ball_speed * math.cos(angle_rad)
                        })
                elif powerup.type == 'gun':
                    paddle.gun_active = True
                    paddle.gun_end_time = pygame.time.get_ticks() + 10000  # 10 seconds
                    print("Shooting Gun!")
                powerups.remove(powerup)
            elif powerup.rect.top > SCREEN_HEIGHT:
                powerups.remove(powerup)

        paddle.update()

        if expand_active and pygame.time.get_ticks() >= expand_end_time:
            paddle.rect.width = original_paddle_width
            expand_active = False

        for ball in balls:
            if ball['rect'].left <= 0:
                ball['rect'].left = 0
                ball['speed_x'] *= -1
            elif ball['rect'].right >= SCREEN_WIDTH:
                ball['rect'].right = SCREEN_WIDTH
                ball['speed_x'] *= -1
            if ball['rect'].top <= UI_HEIGHT:
                ball['rect'].top = UI_HEIGHT
                ball['speed_y'] *= -1

        for ball in balls[:]:
            if ball['rect'].bottom >= SCREEN_HEIGHT:
                balls.remove(ball)

        if not balls:
            lives -= 1
            paddle.gun_active = False  # Reset gun on life loss
            paddle.bullets.clear()
            if lives > 0:
                balls = [{
                    'rect': pygame.Rect(paddle.rect.centerx - ball_radius, paddle.rect.top - ball_radius * 2 - 2, ball_radius * 2, ball_radius * 2),
                    'speed_x': ball_speed,
                    'speed_y': -ball_speed
                }]
            else:
                running = False
                win = False
                final_win = False

        for ball in balls:
            if ball['rect'].colliderect(paddle):
                offset = (ball['rect'].centerx - paddle.rect.centerx) / (paddle.rect.width / 2)
                angle = math.radians(offset * 60)
                ball['speed_x'] = ball_speed * math.sin(angle)
                ball['speed_y'] = -ball_speed * math.cos(angle)

        for ball in balls:
            hit_index = ball['rect'].collidelist([b.rect for b in bricks])
            if hit_index != -1:
                brick = bricks[hit_index]
                if brick.brick_type == 'unbreakable':
                    overlap_x = min(abs(ball['rect'].right - brick.rect.left), abs(ball['rect'].left - brick.rect.right))
                    overlap_y = min(abs(ball['rect'].bottom - brick.rect.top), abs(ball['rect'].top - brick.rect.bottom))

                    if overlap_x < overlap_y:
                        ball['speed_x'] *= -1
                        if ball['rect'].centerx < brick.rect.centerx:
                            ball['rect'].right = brick.rect.left
                        else:
                            ball['rect'].left = brick.rect.right
                    else:
                        ball['speed_y'] *= -1
                        if ball['rect'].centery < brick.rect.centery:
                            ball['rect'].bottom = brick.rect.top
                        else:
                            ball['rect'].top = brick.rect.bottom

                    unbreakable_sound.play()
                    break

                destroyed = brick.hit()
                if destroyed:
                    del bricks[hit_index]
                    if random.random() < 0.3:
                        power_type = random.choice(['expand', 'life', 'multiball', 'gun'])
                        powerups.append(PowerUp(brick.rect.centerx, brick.rect.y, power_type))
                ball['speed_y'] *= -1
                score += 10
                brick_sound.play()
                break

        if not any(b.brick_type != 'unbreakable' for b in bricks):
            next_level_file = f"level{current_level + 1}.json"
            try:
                current_level += 1
                bricks = load_level(next_level_file, brick_width, brick_height, UI_HEIGHT)
                paddle.bullets = []  # Clear existing bullets
                paddle.gun_active = False  # Reset gun ability
                balls = [{
                    'rect': pygame.Rect(paddle.rect.centerx - ball_radius, paddle.rect.top - ball_radius * 2 - 2, ball_radius * 2, ball_radius * 2),
                    'speed_x': ball_speed,
                    'speed_y': -ball_speed
                }]
                powerups = []
                expand_active = False
                paddle.rect.width = original_paddle_width
                paddle.rect.centerx = SCREEN_WIDTH // 2
                show_level_message(screen, current_level, SCREEN_WIDTH, SCREEN_HEIGHT)
            except FileNotFoundError:
                final_win = True
                win = True
                running = False

        screen.fill(BLACK)
        paddle.draw(screen)
        for ball in balls:
            pygame.draw.ellipse(screen, WHITE, ball['rect'])
        for brick in bricks:
            brick.draw(screen)
        for powerup in powerups:
            powerup.draw(screen)
        draw_top_bar(screen, score, lives, SCREEN_WIDTH, UI_HEIGHT)

        if paddle.gun_active:
            elapsed = max(0, paddle.gun_end_time - pygame.time.get_ticks())
            remaining_ratio = elapsed / 10000
            bar_width = int(SCREEN_WIDTH * remaining_ratio)
            pygame.draw.rect(screen, (255, 255, 0), (0, UI_HEIGHT - 5, bar_width, 5))

        paddle.update_bullets(screen, bricks)
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
    show_end_screen(screen, final_win, SCREEN_WIDTH, SCREEN_HEIGHT)
    pygame.quit()
    sys.exit()
