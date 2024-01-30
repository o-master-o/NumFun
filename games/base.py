from abc import ABC, abstractmethod
from typing import Type

from games.utils import get_game_info
from ui.base import UI


class Game(ABC):
    NAME = None

    def __init__(self, ui):
        self.ui = ui
        self._game_info = get_game_info(self.NAME)
        self.ui.display_message(self._game_info['header'])
        self.ui.display_message(self._game_info['description'])
        self.ui.display_message(self._game_info['control'])

    @abstractmethod
    def start(self):
        pass
