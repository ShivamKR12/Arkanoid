import json
import os

from game_objects import Brick


class LevelLoader:
    @staticmethod
    def load(filename, brick_width, brick_height, ui_height):
        with open(os.path.join("levels", filename)) as level_file:
            data = json.load(level_file)

        bricks = []
        for brick_data in data:
            brick = Brick(
                brick_data["x"] * brick_width,
                ui_height + brick_data["y"] * brick_height,
                brick_width - 2,
                brick_height - 2,
                (255, 255, 255) if brick_data["type"] == "multi" else tuple(brick_data["color"]),
                brick_data["type"],
                tuple(brick_data["color"]),
            )
            bricks.append(brick)
        return bricks
