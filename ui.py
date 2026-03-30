import pygame, sys, asyncio

async def show_start_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT):
    font_big = pygame.font.Font(None, 64)
    font_small = pygame.font.Font(None, 36)

    title = font_big.render("Arkanoid Fire Ball", True, (255, 140, 0))
    easy = font_small.render("Press E for Easy Mode", True, (200, 200, 200))
    hard = font_small.render("Press H for Hard Mode", True, (255, 100, 100))

    while True:
        screen.fill((20, 20, 20))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
        screen.blit(easy, (SCREEN_WIDTH // 2 - easy.get_width() // 2, 300))
        screen.blit(hard, (SCREEN_WIDTH // 2 - hard.get_width() // 2, 350))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    return 'easy'
                elif event.key == pygame.K_h:
                    return 'hard'
    
        await asyncio.sleep(0)  # Just to make this function async-compatible

async def show_level_message(screen, level_number, SCREEN_WIDTH, SCREEN_HEIGHT):
    font = pygame.font.Font(None, 72)
    text = font.render(f"Level {level_number}", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
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
        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        clock.tick(60)

        await asyncio.sleep(0)  # Allow other async tasks to run

def draw_top_bar(screen, score, lives, SCREEN_WIDTH, UI_HEIGHT):
    font = pygame.font.Font(None, 36)
    pygame.draw.rect(screen, (30, 30, 30), (0, 0, SCREEN_WIDTH, UI_HEIGHT))

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    title_font = pygame.font.Font(None, 40)
    title_text = title_font.render("Arkanoid Fire Ball", True, (255, 140, 0))

    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))

def show_end_screen(screen, final_win, SCREEN_WIDTH, SCREEN_HEIGHT):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 48)

    if final_win:
        end_text = font.render("You Beat All Levels!", True, (0, 255, 0))
    else:
        end_text = font.render("Game Over!", True, (255, 0, 0))

    screen.blit(end_text, (SCREEN_WIDTH // 2 - end_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
