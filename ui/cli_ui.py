import os
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
import emoji

from ui.base import UI


class CliUI(UI):
    CONGRATULATIONS = f"{emoji.emojize(':smiling_cat_with_heart-eyes:')} Congratulations!"
    COMMISERATIONS = f"{emoji.emojize(':crying_cat:')} Try again!"
    LIGHT_YELLOW = "#ffffbf"

    def __init__(self):
        self._console = Console()

    def reset_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def display_game_introduction(self, game_info):
        introduction = (
            f"[yellow]{game_info['header']}[/]\n"
            f"[bold yellow]Description[/]\n"
            f"[{self.LIGHT_YELLOW}]{game_info['description']}[/]\n"
            f"\n"
            f"[bold yellow]How to Play[/]\n"
            f"[{self.LIGHT_YELLOW}]{game_info['instruction']}[/]\n"
            f"\n"
            f"[bold yellow]Control[/]\n"
            f"[{self.LIGHT_YELLOW}]{game_info['control']}[/]"
        )

        self._console.print(Panel(introduction, expand=False, border_style="yellow"))

    def display_message(self, message):
        self._console.print(f"  {message}")

    def ask_question(self, message):
        return self._console.input(f"{message}")
