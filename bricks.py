import pygame

class Brick:
    def __init__(self, x, y, width, height, color, brick_type, original_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.brick_type = brick_type  # 'breakable', 'unbreakable', 'multi'
        self.original_color = original_color or color
        self.hit_points = 2 if brick_type == 'multi' else 1

    def draw(self, screen):
        if self.brick_type == 'unbreakable':
            pygame.draw.rect(screen, (60, 60, 60), self.rect)  # dark grey
            pygame.draw.line(screen, (120, 120, 120), self.rect.topleft, self.rect.bottomright, 2)
            pygame.draw.line(screen, (120, 120, 120), self.rect.topright, self.rect.bottomleft, 2)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

    def hit(self):
        if self.brick_type == 'unbreakable':
            return False  # Not destroyed

        self.hit_points -= 1

        if self.brick_type == 'multi' and self.hit_points == 1:
            self.color = self.original_color  # Change color at last hit

        return self.hit_points <= 0  # True if brick is destroyed

