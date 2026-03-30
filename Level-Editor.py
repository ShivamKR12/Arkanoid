import pygame
import json
import sys
import os

pygame.init()
screen = pygame.display.set_mode((600, 700), pygame.RESIZABLE)
pygame.display.set_caption("Arkanoid Level Editor")
clock = pygame.time.Clock()

ROWS, COLS = 10, 10
CELL_WIDTH = screen.get_width() // COLS
CELL_HEIGHT = 40

colors = [
    (255, 0, 0),  # Red
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),  # Green
    (0, 255, 255),  # Cyan
    (255, 255, 255)  # White
]
color_index = 0
brick_type = "breakable"

level_number = 1
font = pygame.font.Font(None, 32)

show_help = True  # Toggle control instructions

grid = {}  # (x, y) => {'color': (r,g,b), 'type': 'breakable'}

def draw_grid():
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x * CELL_WIDTH, y * CELL_HEIGHT, CELL_WIDTH - 2, CELL_HEIGHT - 2)
            if (x, y) in grid:
                brick = grid[(x, y)]
                draw_color = brick['color']
                label_char = brick['type'][0].upper()

                if brick['type'] == 'multi':
                    draw_color = (255, 255, 255)  # Force white color
                    label_char = "M"
                elif brick['type'] == 'unbreakable':
                    draw_color = (60, 60, 60)
                    label_char = "U"

                pygame.draw.rect(screen, draw_color, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 2)
                font_small = pygame.font.Font(None, 24)
                text = font_small.render(label_char, True, (0, 0, 0))
                screen.blit(text, rect.center)
            else:
                pygame.draw.rect(screen, (50, 50, 50), rect, 1)

def load_level_file(num):
    filename = f"level{num}.json"
    if os.path.exists(os.path.join("levels", filename)):
        try:
            with open(os.path.join("levels", filename)) as f:
                loaded = json.load(f)
                grid.clear()
                for b in loaded:
                    grid[(b['x'], b['y'])] = {
                        'color': tuple(b['color']),
                        'type': b['type']
                    }
            print(f"Level loaded from {filename}")
        except Exception as e:
            print(f"Could not load {filename}:", e)
    else:
        print(f"No such level: {filename}")

load_level_file(level_number)

running = True
while running:
    screen.fill((30, 30, 30))
    draw_grid()

    level_text = font.render(f"Editing Level {level_number}", True, (255, 255, 255))
    screen.blit(level_text, (10, screen.get_height() - 30))

    if show_help:
        instructions = [
            "Controls:",
            "Left Click   - Place brick",
            "Right Click  - Remove brick",
            "1–6          - Select color",
            "B            - Breakable",
            "M            - Multi-hit",
            "U            - Unbreakable",
            "S            - Save level",
            "L            - Load level",
            "C            - Clear grid",
            "</>          - Switch level",
            "H            - Toggle help"
        ]
        font_small = pygame.font.Font(None, 24)
        for i, line in enumerate(instructions):
            text = font_small.render(line, True, (200, 200, 200))
            screen.blit(text, (10, 410 + i * 22))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            CELL_WIDTH = screen.get_width() // COLS
            CELL_HEIGHT = screen.get_height() // ROWS

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            col = x // CELL_WIDTH
            row = y // CELL_HEIGHT
            if event.button == 1:  # Left click = place
                grid[(col, row)] = {
                    'color': colors[color_index],
                    'type': brick_type
                }
            elif event.button == 3:  # Right click = remove
                grid.pop((col, row), None)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                grid.clear()
            elif event.key == pygame.K_s:
                filename = f"level{level_number}.json"
                with open(filename, "w") as f:
                    data = []
                    for (x, y), brick in grid.items():
                        data.append({
                            "x": x,
                            "y": y,
                            "color": brick['color'],
                            "type": brick['type']
                        })
                    json.dump(data, f, indent=2)
                print(f"Level saved to {filename}")
            elif event.key == pygame.K_l:
                load_level_file(level_number)
            elif event.key == pygame.K_LEFT:
                level_number = max(1, level_number - 1)
                load_level_file(level_number)
            elif event.key == pygame.K_RIGHT:
                level_number += 1
                load_level_file(level_number)
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]:
                color_index = event.key - pygame.K_1
                print(f"Selected color: {colors[color_index]}")
            elif event.key == pygame.K_b:
                brick_type = "breakable"
                print("Brick type: breakable")
            elif event.key == pygame.K_m:
                brick_type = "multi"
                print("Brick type: multi-hit")
            elif event.key == pygame.K_u:
                brick_type = "unbreakable"
                print("Brick type: unbreakable")
            elif event.key == pygame.K_h:
                show_help = not show_help

    clock.tick(60)

pygame.quit()
sys.exit()
