from pathlib import Path

import typer
from typer import Context

from games.manager import GameManager
from games.utils import get_game_info
from ui.cli_ui import CliUI
from ui.gui import GUI
from utils import update_git_repo


class NumFun:
    REPO_PATH = Path(__file__).parent
    INTERFACES = {True: GUI, False: CliUI}

    def game_app(self):

        app = typer.Typer(
            rich_markup_mode='rich',
            name='num-fun',
            help=self._get_console_man(),
            context_settings={"help_option_names": ["-h", "--help"]}
        )

        @app.callback(invoke_without_command=True)
        def main(ctx: Context,
                 gui_flag: bool = typer.Option(False, "--gui", "-g", help="Starts main game interface in graphical mode")):
            if ctx.invoked_subcommand is None:
                GameManager(self.INTERFACES[gui_flag]).start()

        @app.command(name='update', short_help='Update application')
        def update():
            update_git_repo(self.REPO_PATH)

        return app

    def _get_console_man(self):
        info = get_game_info('num-fun')
        header = self._format_header(info['header'])
        return ''.join([header, f"[{CliUI.LIGHT_YELLOW}]", info['description']])

    def _format_header(self, header):
        split_lines = header[1:].split('\n')
        lines = [f"[{CliUI.YELLOW}]{line.strip()}" for line in split_lines]
        return '\n'.join([f"{lines[1]}\n"] + lines[2:])


if __name__ == "__main__":
    NumFun().game_app()()
    # get_console_man()
