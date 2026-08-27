import json
import os
import pygame


class LevelEditor:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 700), pygame.RESIZABLE)
        pygame.display.set_caption("Arkanoid Level Editor")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)

        self.rows, self.columns = 10, 10
        self.cell_width = self.screen.get_width() // self.columns
        self.cell_height = 40

        self.colors = [
            (255, 0, 0),
            (255, 165, 0),
            (255, 255, 0),
            (0, 255, 0),
            (0, 255, 255),
            (255, 255, 255),
        ]
        self.color_index = 0
        self.brick_type = "breakable"
        self.level_number = 1
        self.show_help = True
        self.grid = {}

    def draw_grid(self):
        for y in range(self.rows):
            for x in range(self.columns):
                rect = pygame.Rect(x * self.cell_width, y * self.cell_height, self.cell_width - 2, self.cell_height - 2)
                if (x, y) in self.grid:
                    brick = self.grid[(x, y)]
                    draw_color = brick["color"]
                    label_char = brick["type"][0].upper()

                    if brick["type"] == "multi":
                        draw_color = (255, 255, 255)
                        label_char = "M"
                    elif brick["type"] == "unbreakable":
                        draw_color = (60, 60, 60)
                        label_char = "U"

                    pygame.draw.rect(self.screen, draw_color, rect)
                    pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
                    font_small = pygame.font.Font(None, 24)
                    text = font_small.render(label_char, True, (0, 0, 0))
                    self.screen.blit(text, text.get_rect(center=rect.center))
                else:
                    pygame.draw.rect(self.screen, (50, 50, 50), rect, 1)

    def load_level_file(self, num):
        filename = f"level{num}.json"
        if os.path.exists(os.path.join("levels", filename)):
            try:
                with open(os.path.join("levels", filename)) as level_file:
                    loaded = json.load(level_file)
                    self.grid.clear()
                    for brick in loaded:
                        self.grid[(brick["x"], brick["y"])] = {
                            "color": tuple(brick["color"]),
                            "type": brick["type"],
                        }
                print(f"Level loaded from {filename}")
            except Exception as exc:
                print(f"Could not load {filename}: {exc}")
        else:
            print(f"No such level: {filename}")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self.cell_width = self.screen.get_width() // self.columns
                self.cell_height = self.screen.get_height() // self.rows

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // self.cell_width
                row = y // self.cell_height
                if event.button == 1:
                    self.grid[(col, row)] = {"color": self.colors[self.color_index], "type": self.brick_type}
                elif event.button == 3:
                    self.grid.pop((col, row), None)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    self.grid.clear()
                elif event.key == pygame.K_s:
                    filename = f"level{self.level_number}.json"
                    with open(os.path.join("levels", filename), "w") as level_file:
                        data = []
                        for (x, y), brick in self.grid.items():
                            data.append({"x": x, "y": y, "color": brick["color"], "type": brick["type"]})
                        json.dump(data, level_file, indent=2)
                    print(f"Level saved to {filename}")
                elif event.key == pygame.K_l:
                    self.load_level_file(self.level_number)
                elif event.key == pygame.K_LEFT:
                    self.level_number = max(1, self.level_number - 1)
                    self.load_level_file(self.level_number)
                elif event.key == pygame.K_RIGHT:
                    self.level_number += 1
                    self.load_level_file(self.level_number)
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]:
                    self.color_index = event.key - pygame.K_1
                    print(f"Selected color: {self.colors[self.color_index]}")
                elif event.key == pygame.K_b:
                    self.brick_type = "breakable"
                    print("Brick type: breakable")
                elif event.key == pygame.K_m:
                    self.brick_type = "multi"
                    print("Brick type: multi-hit")
                elif event.key == pygame.K_u:
                    self.brick_type = "unbreakable"
                    print("Brick type: unbreakable")
                elif event.key == pygame.K_h:
                    self.show_help = not self.show_help

        return True

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.draw_grid()

        level_text = self.font.render(f"Editing Level {self.level_number}", True, (255, 255, 255))
        self.screen.blit(level_text, (10, self.screen.get_height() - 30))

        if self.show_help:
            instructions = [
                "Controls:",
                "Left Click   - Place brick",
                "Right Click  - Remove brick",
                "1-6          - Select color",
                "B            - Breakable",
                "M            - Multi-hit",
                "U            - Unbreakable",
                "S            - Save level",
                "L            - Load level",
                "C            - Clear grid",
                "</>          - Switch level",
                "H            - Toggle help",
            ]
            font_small = pygame.font.Font(None, 24)
            for i, line in enumerate(instructions):
                text = font_small.render(line, True, (200, 200, 200))
                self.screen.blit(text, (10, 410 + i * 22))

        pygame.display.flip()

    def run(self):
        self.load_level_file(self.level_number)
        running = True
        while running:
            self.draw()
            running = self.handle_events()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    LevelEditor().run()
