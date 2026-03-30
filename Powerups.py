import pygame

class PowerUp:
    def __init__(self, x, y, type):
        self.type = type  # 'expand', 'life', 'multiball', 'gun'
        self.rect = pygame.Rect(x, y, 30, 30)
        self.speed = 4
        self.color = self.get_color()

    def get_color(self):
        return {
            'expand': (0, 255, 0),       # Green
            'life': (255, 0, 0),         # Red
            'multiball': (0, 255, 255),  # Cyan
            'gun': (255, 255, 0)         # Yellow
        }[self.type]

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 24)
        text = font.render(self.type[0].upper(), True, (0, 0, 0))
        screen.blit(text, (self.rect.x + 8, self.rect.y + 5))