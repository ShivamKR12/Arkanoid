import json
import os
from game_objects import Brick


def load_level(filename, brick_width, brick_height, UI_HEIGHT):
    with open(os.path.join("levels", filename)) as f:
        data = json.load(f)
        bricks = []
        for b_data in data:
            brick = Brick(
                b_data['x'] * brick_width,
                UI_HEIGHT + b_data['y'] * brick_height,
                brick_width - 2,
                brick_height - 2,
                (255, 255, 255) if b_data['type'] == 'multi' else tuple(b_data['color']),
                b_data['type'],
                tuple(b_data['color'])
            )
            bricks.append(brick)
        return bricks
