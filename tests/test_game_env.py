import unittest

from the_game.game_env import GameEnv, Player


class TestPlayer(Player):
    def play(self):
        for card in sorted(self.hand):
            for heap in self.upward_heaps + self.downward_heaps:
                if self.play_card(card, heap) is True:
                    break

    def game_over(self, score):
        super().game_over(score)
        print(f"Final score is: {score}")


class TestGameEnv(unittest.TestCase):
    game_env = None

    def setUp(self) -> None:
        super().setUp()
        self.game_env = GameEnv()
        self.game_env.add_player(TestPlayer)

    def test_game(self):
        self.game_env.play_game()


if __name__ == "__main__":
    unittest.main()
