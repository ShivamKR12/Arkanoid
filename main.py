# /// script
# dependencies = [
#     "pygame-ce",
# ]
# ///

import asyncio
from game_manager import Game


if __name__ == '__main__':
    game = Game()
    asyncio.run(game.run())
