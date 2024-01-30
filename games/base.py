from abc import ABC, abstractmethod

from games.utils import get_game_info


class Game(ABC):
    NAME = None

    def __init__(self, ui):
        self.ui = ui
        self._game_info = get_game_info(self.NAME)
        self.ui.display_game_introduction(self._game_info)
        self.ui.display_game_interface(self._game_info)


    @property
    def game_info(self):
        return self._game_info

    @abstractmethod
    def start(self):
        pass

    # def _show_game_interface(self):
    #     self.ui.display_message(Panel(f"\n  [yellow]{self._game_info['header']}[/]\n"
    #                             f"  [bold yellow]Control[/]\n"
    #                             f"  [{self.ui.LIGHT_YELLOW}]{self._game_info['control']}[/]")
    #                             )
