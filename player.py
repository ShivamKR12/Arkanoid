import pygame
import time
import os

class Paddle:
    def __init__(self, x, y, width, height, screen_width):
        self.rect = pygame.Rect(x, y, width, height)
        self.original_width = width
        self.speed = 10
        self.screen_width = screen_width

        # Gun / shooting logic
        self.bullets = []
        self.gun_active = False
        self.gun_cooldown = 400  # milliseconds
        self.gun_end_time = 0  # Timestamp when gun should deactivate
        self.last_shot_time = 0

        sound_path = os.path.join('assets', 'sounds', 'brick_hit.ogg')
        self.brick_sound = pygame.mixer.Sound(sound_path)

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < self.screen_width:
            self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

        # Draw bullets
        for bullet in self.bullets:
            pygame.draw.rect(screen, (255, 255, 0), bullet)

        # Optional: flash lines for gun firing
        if self.gun_active and pygame.time.get_ticks() - self.last_shot_time < 100:
            pygame.draw.line(screen, (255, 255, 0), (self.rect.left + 5, self.rect.top),
                                 (self.rect.left + 5, self.rect.top - 10), 2)
            pygame.draw.line(screen, (255, 255, 0), (self.rect.right - 9, self.rect.top),
                                 (self.rect.right - 9, self.rect.top - 10), 2)

    def activate_expand(self):
        self.rect.width = int(self.original_width * 1.5)
        self.rect.centerx = max(self.rect.width // 2, min(self.rect.centerx, self.screen_width - self.rect.width // 2))

    def reset_width(self):
        self.rect.width = self.original_width

    def activate_gun(self):
        self.gun_active = True
        self.last_shot_time = pygame.time.get_ticks()  # reset cooldown

    # One bullet
    # def shoot(self):
    #     current_time = pygame.time.get_ticks()
    #     if self.gun_active and current_time - self.last_shot_time > self.gun_cooldown:
    #         bullet = pygame.Rect(self.rect.centerx - 2, self.rect.top - 10, 4, 10)
    #         self.bullets.append(bullet)
    #         self.last_shot_time = current_time

    # Two bullets
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if self.gun_active and current_time - self.last_shot_time > self.gun_cooldown:
            left_bullet = pygame.Rect(self.rect.left + 5, self.rect.top - 10, 4, 10)
            right_bullet = pygame.Rect(self.rect.right - 9, self.rect.top - 10, 4, 10)
            self.bullets.append(left_bullet)
            self.bullets.append(right_bullet)
            self.last_shot_time = current_time
            return True  # Shot was fired
        return False  # No shot

    def update_bullets(self, screen, bricks):
        for bullet in self.bullets[:]:
            bullet.y -= 10
            pygame.draw.rect(screen, (255, 0, 0), bullet)

            if bullet.bottom < 0:
                self.bullets.remove(bullet)
                continue

            hit_index = bullet.collidelist([b.rect for b in bricks])
            if hit_index != -1:
                brick = bricks[hit_index]
                if brick.brick_type != 'unbreakable':
                    destroyed = brick.hit()
                    # self.brick_sound.play()
                    if destroyed:
                        del bricks[hit_index]
                self.bullets.remove(bullet)
    def update(self):
        if self.gun_active and pygame.time.get_ticks() > self.gun_end_time:
            self.gun_active = False
