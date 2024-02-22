

from num_fun.ui.base import UI


class GUI(UI):
    BOLD_RED = "\x1b[31;1m"
    NC = "\x1b[0m"

    def __init__(self):
        print(f"{self.BOLD_RED}GUI interface is under development. Please use CLI interface{self.NC}")
        exit(0)

    def reset_screen(self):
        pass

    def display_game_introduction(self, message):
        pass

    def ask_user_to_select_game(self, games_names):
        pass

    def display_message(self, message):
        pass

    def ask_question(self, message):
        pass