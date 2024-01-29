from typing import Protocol

from ui.base import UI


class Game(Protocol):
    ui: UI

    def start(self):
        pass

    def stop(self):
        pass
