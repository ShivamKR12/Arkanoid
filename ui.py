import asyncio
import pygame


class GameUI:
    def __init__(self, screen):
        self.screen = screen
        self.font_big = pygame.font.Font(None, 64)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.font_hs = pygame.font.Font(None, 42)

    async def show_start_screen(self, high_score):
        while True:
            self.screen.fill((20, 20, 20))

            title = self.font_big.render("Arkanoid Fire Ball", True, (255, 140, 0))
            easy = self.font_small.render("Press E for Easy Mode", True, (200, 200, 200))
            hard = self.font_small.render("Press H for Hard Mode", True, (255, 100, 100))
            high_score_text = self.font_hs.render(f"High Score: {high_score}", True, (255, 215, 0))

            self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 200))
            self.screen.blit(high_score_text, (self.screen.get_width() // 2 - high_score_text.get_width() // 2, 270))
            self.screen.blit(easy, (self.screen.get_width() // 2 - easy.get_width() // 2, 300))
            self.screen.blit(hard, (self.screen.get_width() // 2 - hard.get_width() // 2, 350))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        return "easy"
                    if event.key == pygame.K_h:
                        return "hard"

            await asyncio.sleep(0)

    async def show_level_message(self, level_number, screen_width, screen_height):
        font = pygame.font.Font(None, 72)
        text = font.render(f"Level {level_number}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))

        overlay = pygame.Surface((screen_width, screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(0)

        clock = pygame.time.Clock()
        start_ticks = pygame.time.get_ticks()
        fade_duration = 1500

        while True:
            elapsed = pygame.time.get_ticks() - start_ticks
            if elapsed > fade_duration:
                break

            alpha = int(255 * (1 - (elapsed / fade_duration)))
            overlay.set_alpha(alpha)
            self.screen.fill((0, 0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(overlay, (0, 0))
            pygame.display.flip()
            clock.tick(60)
            await asyncio.sleep(0)

    def draw_top_bar(self, score, lives, screen_width, ui_height):
        font = pygame.font.Font(None, 36)
        pygame.draw.rect(self.screen, (30, 30, 30), (0, 0, screen_width, ui_height))

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
        title_font = pygame.font.Font(None, 40)
        title_text = title_font.render("Arkanoid Fire Ball", True, (255, 140, 0))

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (screen_width - 120, 10))
        self.screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 10))

    def show_end_screen(self, final_win, score, new_high_score, screen_width, screen_height):
        self.screen.fill((0, 0, 0))

        if final_win:
            end_text = self.font_big.render("You Beat All Levels!", True, (0, 255, 0))
        else:
            end_text = self.font_big.render("Game Over!", True, (255, 0, 0))

        score_text = self.font_medium.render(f"Final Score: {score}", True, (255, 255, 255))
        self.screen.blit(end_text, (screen_width // 2 - end_text.get_width() // 2, screen_height // 2 - 50))
        self.screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 + 20))

        if new_high_score:
            new_hs_text = self.font_medium.render("New High Score!", True, (255, 215, 0))
            self.screen.blit(new_hs_text, (screen_width // 2 - new_hs_text.get_width() // 2, screen_height // 2 + 70))

        pygame.display.flip()
        pygame.time.wait(3000)
