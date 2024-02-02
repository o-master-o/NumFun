from pathlib import Path

import typer
from typer import Context

from games.manager import GameManager
from games.utils import get_game_info
from ui.cli_ui import CliUI
from ui.gui import GUI
from utils import update_git_repo

REPO_PATH = Path(__file__).parent
INTERFACES = {True: GUI, False: CliUI}


def _format_text(text):
    print(type(text))
    print(text.split('\n'))


def get_console_man():
    info = get_game_info('num-fun')
    return (f"{info['header']}\n"
            f"{info['description']}")


def game_app():

    app = typer.Typer(
        rich_markup_mode='rich',
        name='num-fun',
        help=get_console_man()
    )

    @app.callback(invoke_without_command=True)
    def main(ctx: Context,
             gui_flag: bool = typer.Option(False, "--gui", "-g", help="Starts main game interface in graphical mode")):
        if ctx.invoked_subcommand is None:
            GameManager(INTERFACES[gui_flag]).start()

    @app.command(name='update', short_help='Update application')
    def update():
        update_git_repo(REPO_PATH)

    return app


if __name__ == "__main__":
    game_app()()
