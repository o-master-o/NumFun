from abc import ABC, abstractmethod
from typing import Type

from ui.base import UI


class Game(ABC):
    NAME = None
    HEADER = ''

    def __init__(self, ui):
        self.ui = ui
        self.ui.display_message(self.HEADER)

    @abstractmethod
    def start(self):
        pass
