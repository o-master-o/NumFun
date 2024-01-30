from prompt_toolkit import prompt

from games.calculator import Calculator
from games.digit_detective import DigitDetective
from games.x_pedition import Xpedition
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter

from games.utils import get_game_info

games_list = [Xpedition, DigitDetective, Calculator]


class GamesPocket:

    def __init__(self, games):
        self._games = {}
        self._register_games(games)

    def _register_games(self, games):
        for g in games:
            self._games.update({g.NAME: g})

    @property
    def names(self):
        return self._games.keys()

    def get(self, game_name):
        game = self._games.get(game_name)
        if game is None:
            print("Game not found.")
            return None
        else:
            return game


class GameManager:
    def __init__(self, ui, ):
        self.ui = ui()
        self._games_pocket = GamesPocket(games_list)

    def start(self):
        info = get_game_info('num-fun')
        play = True
        while play:
            self.ui.reset_screen()
            self.ui.display_message(info['header'])
            play = self._choose_and_play_game()

    def _choose_and_play_game(self):
        try:
            self._play_game(self._choose_game(self._games_pocket.names))
            return True
        except KeyboardInterrupt:
            print('Exit Numfun')
            return False

    def _choose_game(self, games_names):
        game_completer = WordCompleter(games_names)
        self.ui.display_message("[bold yellow]Control:[/] Press [yellow]TAB[/] to choose a game, press [yellow]Ctrl+C[/] to Exit")
        selected_game_name = prompt("Choose a game: ", completer=game_completer, style=Style([('prompt', 'fg:ansiyellow')]))
        return self._games_pocket.get(selected_game_name)

    def _play_game(self, game):
        self.ui.reset_screen()
        try:
            game(ui=self.ui).start()
        except KeyboardInterrupt:
            self.ui.display_message(f'[yellow]Exit game [bold]{game.NAME}[/]')
            return

