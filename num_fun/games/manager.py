from num_fun.games.utils import get_game_info


class GamesPocket:

    def __init__(self, games):
        self._games = {}
        self._register_games(games)

    def _register_games(self, games):
        for g in games:
            self._games.update({g.NAME: g})

    @property
    def names(self):
        return list(self._games.keys())

    def get(self, game_name):
        return self._games.get(game_name)


class GameManager:
    def __init__(self, ui, games_list):
        self.ui = ui()
        self._games_pocket = GamesPocket(games_list)
        self._selected_game = None

    def start(self):
        info = get_game_info('num-fun')
        play = True
        while play:
            self.ui.reset_screen()
            self.ui.display_message(info['header'])
            play = self._choose_and_play_game()

    def _choose_and_play_game(self):
        try:
            selected_game_name = self.ui.ask_user_to_select_game(self._games_pocket.names)
            self._selected_game = self._games_pocket.get(selected_game_name)
            self._play_game()
            return True
        except KeyboardInterrupt:
            self._exit_num_fun()
            return False
        finally:
            self._selected_game = None

    def _play_game(self):
        self.ui.reset_screen()
        try:
            game = self._selected_game(ui=self.ui)
            while True:
                game.start()
        except KeyboardInterrupt:
            self.ui.display_message(f'\n[yellow]Exit game [bold]{self._selected_game.NAME}[/]')
            return

    def _exit_num_fun(self):
        self.ui.reset_screen()
        self.ui.display_message('\n[yellow] You left the game [b]NumFun[not b]. \n '
                                'See you Later. 😉 Bye.. \n[/]')
