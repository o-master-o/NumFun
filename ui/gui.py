

from ui.base import UI


class GUI(UI):

    def reset_screen(self):
        print('1')

    def display_message(self, message):
        print(message)

    def ask_question(self, message):
        return input(message)
