from abc import ABC, abstractmethod

from games.utils import get_game_info


class Game(ABC):
    NAME = None

    def __init__(self, ui):
        self.ui = ui
        self._game_info = get_game_info(self.NAME)
        self.ui.display_game_introduction(self._game_info)

    @property
    def game_info(self):
        return self._game_info

    @abstractmethod
    def start(self):
        pass
