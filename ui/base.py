from abc import ABC, abstractmethod


class UI(ABC):

    @abstractmethod
    def reset_screen(self):
        pass

    @abstractmethod
    def display_game_introduction(self, message):
        pass

    @abstractmethod
    def display_message(self, message):
        pass

    @abstractmethod
    def ask_question(self, message):
        pass
