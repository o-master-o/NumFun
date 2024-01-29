from typing import Type
from games.base import Game
from prompt_toolkit import prompt
from ui.base import UI
from prompt_toolkit.completion import WordCompleter


class GameManager:
    def __init__(self, ui: Type[UI]):
        self.ui = ui

    def choose_game(self, games_list: dict[str, Type[Game]]) -> None:

        game_completer = WordCompleter(list(games_list.keys()))
        selected_game = prompt("Choose a game: ", completer=game_completer)

        if selected_game in games_list:
            game_instance = games_list[selected_game](ui=self.ui)
            game_instance.start()
        else:
            print("Game not found.")


