from abc import ABC, abstractmethod
from typing import Type

from ui.base import UI


class Game(ABC):
    def __init__(self, ui: Type[UI]):
        self.ui = ui()

    @abstractmethod
    def start(self):
        pass
