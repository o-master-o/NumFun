from typing import Type
from games.base import Game
from prompt_toolkit import prompt

from games.calculator import Calculator
from games.digit_detective import DigitDetective
from games.x_pedition import Xpedition
from ui.base import UI
from prompt_toolkit.completion import WordCompleter


games_map = {
    "x-pedition": Xpedition,
    "digit-detective": DigitDetective,
    "calculator": Calculator
}


class GameManager:
    def __init__(self, ui: Type[UI]):
        self.ui = ui

    def start(self):
        while True:
            self._choose_and_play_game()

    def _choose_and_play_game(self):
        try:
            self._play_game(self._choose_game(games_map))
        except KeyboardInterrupt:
            print('Exit game')

    def _choose_game(self, games_map: dict[str, Type[Game]]) -> Type[Game]:
        game_completer = WordCompleter(list(games_map.keys()))
        selected_game = prompt("Choose a game: ", completer=game_completer)
        game = games_map.get(selected_game)
        if game is None:
            print("Game not found.")
        else:
            return game

    def _play_game(self, game):
        game(ui=self.ui).start()
