import os
from rich.panel import Panel
from rich.console import Console
import emoji

from ui.base import UI


class CliUI(UI):
    CONGRATULATIONS = f"{emoji.emojize(':smiling_cat_with_heart-eyes:')} Congratulations!"
    COMMISERATIONS = f"{emoji.emojize(':crying_cat:')} Try again!"

    def __init__(self):
        self._console = Console()

    def reset_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def display_message(self, message):
        self._console.print(f"  {message}")

    def ask_question(self, message):
        return self._console.input(f"  {message}")
