import pygame
import math
import random

class Ball:
    def __init__(self, x, y, radius, speed):
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.radius = radius
        self.base_speed = speed
        self.speed_x = speed
        self.speed_y = -speed

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def draw(self, screen):
        pygame.draw.ellipse(screen, (255, 255, 255), self.rect)

    def normalize_speed(self):
        current_speed = math.sqrt(self.speed_x**2 + self.speed_y**2)
        if current_speed > 0:
            scale = self.base_speed / current_speed
            self.speed_x *= scale
            self.speed_y *= scale

    def handle_collision(self, other_rect, prev_rect):
        intersection = self.rect.clip(other_rect)

        if intersection.width < intersection.height:
            # Horizontal collision
            if prev_rect.right <= other_rect.left:
                self.rect.right = other_rect.left
                self.speed_x = -abs(self.speed_x)
            elif prev_rect.left >= other_rect.right:
                self.rect.left = other_rect.right
                self.speed_x = abs(self.speed_x)
            self.speed_y += random.uniform(-0.1, 0.1) # Add variation
        else:
            # Vertical collision
            if prev_rect.bottom <= other_rect.top:
                self.rect.bottom = other_rect.top
                self.speed_y = -abs(self.speed_y)
            elif prev_rect.top >= other_rect.bottom:
                self.rect.top = other_rect.bottom
                self.speed_y = abs(self.speed_y)
            self.speed_x += random.uniform(-0.1, 0.1) # Add variation

        self.normalize_speed()


class Paddle:
    def __init__(self, x, y, width, height, screen_width):
        self.rect = pygame.Rect(x, y, width, height)
        self.original_width = width
        self.speed = 10
        self.screen_width = screen_width

        # Gun logic
        self.bullets = []
        self.gun_active = False
        self.gun_duration = 10000  # 10 seconds
        self.gun_end_time = 0
        self.gun_cooldown = 400
        self.last_shot_time = 0

        # Expand logic
        self.expand_active = False
        self.expand_duration = 10000 # 10 seconds
        self.expand_end_time = 0

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < self.screen_width:
            self.rect.x += self.speed
        self.rect.clamp_ip(pygame.Rect(0, 0, self.screen_width, 800))

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        for bullet in self.bullets:
            pygame.draw.rect(screen, (255, 255, 0), bullet)

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.gun_active and current_time > self.gun_end_time:
            self.gun_active = False
        if self.expand_active and current_time > self.expand_end_time:
            self.reset_width()
            self.expand_active = False

    def activate_expand(self):
        if not self.expand_active:
            self.rect.width = int(self.original_width * 1.5)
        self.expand_active = True
        self.expand_end_time = pygame.time.get_ticks() + self.expand_duration

    def reset_width(self):
        self.rect.width = self.original_width

    def activate_gun(self):
        self.gun_active = True
        self.gun_end_time = pygame.time.get_ticks() + self.gun_duration

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if self.gun_active and current_time - self.last_shot_time > self.gun_cooldown:
            self.bullets.append(pygame.Rect(self.rect.left + 5, self.rect.top - 10, 4, 10))
            self.bullets.append(pygame.Rect(self.rect.right - 9, self.rect.top - 10, 4, 10))
            self.last_shot_time = current_time
            return True
        return False

    def update_bullets(self, bricks):
        destroyed_bricks = []
        for bullet in self.bullets[:]:
            bullet.y -= 10
            if bullet.bottom < 0:
                self.bullets.remove(bullet)
                continue

            hit_index = bullet.collidelist([b.rect for b in bricks])
            if hit_index != -1:
                brick = bricks[hit_index]
                if brick.brick_type != 'unbreakable':
                    if brick.hit():
                        destroyed_bricks.append(bricks.pop(hit_index))
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
        return destroyed_bricks

    def handle_ball_collision(self, ball):
        offset = (ball.rect.centerx - self.rect.centerx) / (self.rect.width / 2)
        angle = math.radians(offset * 60)
        ball.speed_x = ball.base_speed * math.sin(angle)
        ball.speed_y = -ball.base_speed * math.cos(angle)
        ball.rect.bottom = self.rect.top
        ball.normalize_speed()

    def draw_gun_timer(self, screen, screen_width, ui_height):
        elapsed = max(0, self.gun_end_time - pygame.time.get_ticks())
        ratio = elapsed / self.gun_duration
        bar_width = int(screen_width * ratio)
        pygame.draw.rect(screen, (255, 255, 0), (0, ui_height - 5, bar_width, 5))

    def reset(self):
        self.reset_width()
        self.gun_active = False
        self.expand_active = False
        self.bullets.clear()
        self.rect.centerx = self.screen_width // 2


class Brick:
    def __init__(self, x, y, width, height, color, brick_type, original_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.brick_type = brick_type
        self.original_color = original_color or color
        self.hit_points = 2 if brick_type == 'multi' else 1
        self.score_value = self.get_score_value()

    def get_score_value(self):
        if self.brick_type == 'multi':
            return 25
        elif self.brick_type == 'breakable':
            return 10
        return 0

    def draw(self, screen):
        if self.brick_type == 'unbreakable':
            pygame.draw.rect(screen, (60, 60, 60), self.rect)
            pygame.draw.line(screen, (120, 120, 120), self.rect.topleft, self.rect.bottomright, 2)
            pygame.draw.line(screen, (120, 120, 120), self.rect.topright, self.rect.bottomleft, 2)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

    def hit(self):
        if self.brick_type == 'unbreakable':
            return False
        self.hit_points -= 1
        if self.brick_type == 'multi' and self.hit_points == 1:
            self.color = self.original_color
        return self.hit_points <= 0


class PowerUp:
    def __init__(self, x, y, type):
        self.type = type
        self.rect = pygame.Rect(x - 15, y, 30, 30)
        self.speed = 4
        self.color = self.get_color()
        self.font = pygame.font.Font(None, 24)
        self.text = self.font.render(self.type[0].upper(), True, (0, 0, 0))

    def get_color(self):
        return {'expand': (0, 255, 0), 'life': (255, 0, 0), 'multiball': (0, 255, 255), 'gun': (255, 255, 0)}[self.type]

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text, self.text.get_rect(center=self.rect.center))