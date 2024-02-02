import os
import sys

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from rich.panel import Panel
from rich.console import Console
import emoji

from games.utils import get_game_info
from ui.base import UI


class CliUI(UI):
    CONGRATULATIONS = f"{emoji.emojize(':smiling_cat_with_heart-eyes:')} Congratulations!\n"
    COMMISERATIONS = f"{emoji.emojize(':crying_cat:')} Try again!"
    LIGHT_YELLOW = "#ffffbf"

    def __init__(self):
        self._console = Console()

    def reset_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def display_game_introduction(self, game_info):
        common_info = get_game_info('common')
        introduction = (
            f"{game_info['header']}[/]\n"
            f"{common_info['game-sub-header']}[/]\n\n"
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
        self.ask_question('')
        self.reset_screen()

    def display_game_interface(self, game_info):
        header = (
            f"[yellow]{game_info['header']}[/]\n"
            f"[bold yellow]Control[/]\n"
            f"[{self.LIGHT_YELLOW}]{game_info['control']}[/]"
        )

        self._console.print(Panel(header, expand=False, border_style="yellow"))

    def ask_user_to_select_game(self, games_names):
        self.display_message("[bold yellow]Control:[/] Press [yellow]TAB[/] to choose a game, press [yellow]Ctrl+C[/] to Exit\n")
        while True:
            selected_game_name = prompt("  Choose a game: ", completer=WordCompleter(games_names), style=Style([('prompt', 'fg:ansiyellow')]))
            if selected_game_name in games_names:
                return selected_game_name
            self._remove_last_lines()

    def display_message(self, message):
        self._console.print(self._format_message(message))

    def ask_question(self, message):
        return self._console.input(self._format_message(message))

    def _format_message(self, message):
        return '\n  '.join(''.join(['  ', message]).split('\n'))

    def _remove_last_lines(self, num_lines=1):
        for _ in range(num_lines):
            sys.stdout.write("\033[A")
            sys.stdout.write("\033[K")
        sys.stdout.flush()
