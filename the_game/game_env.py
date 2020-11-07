import collections
import itertools
import random
from typing import List, Optional, Set, Type


class Player:
    def __init__(self, game_env: "GameEnv"):
        """
        Init Player. Draw 'draw_count' number of cards from 'game_env'.
        :param game_env: game environment where we play.
        :type game_env: GameEnv
        """

        self.game_env: GameEnv = game_env
        self.draw_count: int = 0
        self.hand: Set[int] = set()

    @property
    def upward_heaps(self) -> tuple:
        return self.game_env.heaps.get(Heap.HEAP_UP)

    @property
    def downward_heaps(self) -> tuple:
        return self.game_env.heaps.get(Heap.HEAP_DOWN)

    def play(self):
        """
        Play every cards as possible.
        At the end, game env check number of played cards.
        :return:
        :rtype:
        """
        raise NotImplementedError

    def play_card(self, card: int, heap: "Heap") -> bool:
        """
        Try to play a card on given heap.
        :param card: card to play.
        :type card: int
        :param heap: heap where to play given card.
        :type heap: Heap
        :return: True if card has been played correctly.
        :rtype: bool
        """
        if card not in self.hand or heap.validate_card(card) is False:
            return False

        heap.play_card(card)
        self.hand.remove(card)

        return True

    def fill_hand(self) -> int:
        """
        Draw cards and prepare to play.
        :return: number of drawn cards.
        :rtype: int
        """
        total_drawn = 0

        while self.game_env.remaining_cards > 0 and len(self.hand) < self.draw_count:
            self.hand.add(self.game_env.draw_card())
            total_drawn += 1

        return total_drawn

    def game_over(self, score):
        """
        Transmit final score to player.
        Game is over.
        :param score:
        :type score:
        :return:
        :rtype:
        """
        return


class Heap:
    HEAP_UP = "up"
    HEAP_DOWN = "down"

    def __init__(self, direction: str):
        assert direction in (self.HEAP_UP, self.HEAP_DOWN), "Invalid direction."

        self.direction = direction

        if direction == self.HEAP_UP:
            self.heap: List[int] = [1]
        else:
            self.heap: List[int] = [100]

    def validate_card(self, card: int) -> bool:
        """
        Check if given card can be played on this heap.
        :param card: card to validate.
        :type card: int
        :return: True if card can be played here.
        :rtype: bool
        """

        if self.direction == self.HEAP_UP:
            return card > self.heap[0] or card == self.heap[0] - 10
        else:
            return card < self.heap[0] or card == self.heap[0] + 10

    def play_card(self, card: int):
        """
        Play given card on the heap.
        :param card: card to add on the heap.
        :type card: int
        :return:
        :rtype:
        """
        assert self.validate_card(card), "Card cannot be played here."
        self.heap.insert(0, card)


class GameOver(Exception):
    """
    Raise on end of game.
    """


class GameEnv:
    # { num_players: hand_size }
    PLAYER_DRAW_COUNT = collections.defaultdict(
        lambda: 6,
        {
            1: 8,
            2: 7,
        },
    )

    def __init__(self):

        self._deck: list = [x for x in range(2, 100)]

        # shuffle deck
        for _ in range(random.randint(1, 10)):
            random.shuffle(self._deck)

        # init heaps: 2 upward and 2 downward
        self.heaps = {
            Heap.HEAP_UP: tuple(Heap(direction=Heap.HEAP_UP) for _ in range(2)),
            Heap.HEAP_DOWN: tuple(Heap(direction=Heap.HEAP_DOWN) for _ in range(2)),
        }

        # players: 1 to 5 (included)
        self.players: List[Player] = []
        self.current_player_index: int = 0

        # statistics
        self.drawn_cards: int = 0

    @property
    def heap_list(self) -> List[Heap]:
        """
        List of all heaps.
        :return:
        :rtype:
        """
        return list(itertools.chain(*list(self.heaps.values())))

    @property
    def remaining_cards(self):
        """
        Count remaining cards in deck.
        :return:
        :rtype:
        """
        return len(self._deck)

    @property
    def played_cards(self) -> int:
        """
        Count played cards on heaps.
        :return:
        :rtype:
        """
        return sum(map(lambda x: len(x.heap), self.heap_list))

    def calculate_score(self):
        """
        Calculate current score according to played cards.
        :return:
        :rtype:
        """
        score = self.played_cards
        score += max(0, 10 - self.remaining_cards) * 2

        if self.remaining_cards == 0:
            score += 50

        return score

    def add_player(self, player_model: Type[Player]) -> Player:
        """
        Create a new player from given model and add it to game players.
        Then, return it.
        :param player_model: player class inherited from Player.
        :type player_model: Type[Player]
        :return: new created player
        :rtype: Player
        """
        assert issubclass(
            player_model, Player
        ), "'player_model' must inherit from Player class"
        new_player = player_model(game_env=self)
        self.players.append(new_player)
        return new_player

    def prepare_game(self):
        """
        Prepare players for the game.
        :return:
        :rtype:
        """
        # setup players hands
        for player in self.players:
            player.draw_count = self.PLAYER_DRAW_COUNT[len(self.players)]
            player.fill_hand()

    def play_game(self):
        """
        Start game and play until the end.
        :return:
        :rtype:
        """

        assert 1 <= len(self.players) <= 5, "Invalid number of players."

        self.prepare_game()

        # core loop of game
        # break on GameOver or if all cards have been played
        while sum(map(lambda x: len(x.hand), self.players)) > 0:
            try:
                self.play_current_player()
            except GameOver:
                break

        score = self.calculate_score()
        for player in self.players:
            player.game_over(score)

    def play_current_player(self):
        """
        Allow current player to play. Then, select next player.
        :return:
        :rtype:
        """

        current_player = self.players[self.current_player_index]
        self.current_player_index += 1
        self.current_player_index %= len(self.players)

        if len(current_player.hand) > 0:

            total_played_cards = self.played_cards
            current_player.play()
            player_played_cards = self.played_cards - total_played_cards

            # check number of cards played by current player
            if (self.remaining_cards > 0 and player_played_cards < 2) or (
                player_played_cards == 0
            ):
                raise GameOver

            # fill current player hand
            current_player.fill_hand()

    def draw_card(self) -> Optional[int]:
        """
        Draw a card from deck.
        If deck is empty, return None.
        :return: card, or None if empty.
        :rtype: int
        """
        if len(self._deck) > 0:
            self.drawn_cards += 1
            return self._deck.pop()
