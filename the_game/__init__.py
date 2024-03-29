"""
Project package.
"""

from the_game.game_env import GameEnv, Heap, Player

__package_name__ = "the_game"
__description__ = "Core package to simulate 'The Game' game."
__author__ = "Swelio"
__version__ = "0.0.1"
__license__ = "Apache-2.0"
__url__ = "https://github.com/Swelio/TheGameEnv.git"

__all__ = [
    "GameEnv",
    "Heap",
    "Player",
]
