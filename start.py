#!/home/yoda/work/python_projects/NumFun/venv/bin/python
import typer
from typer import Context

from games import x_pedition, digit_detective, calculator
from games.manager import GameManager
from games.utils import get_game_info
from ui.cli_ui import CliUI
from ui.gui import GUI

INTERFACES = { True: GUI, False: CliUI}


def game_app():
    info = get_game_info('num-fun')

    app = typer.Typer(
        rich_markup_mode='rich',
        name='num-fun',
        help=info['header']
    )

    @app.callback(invoke_without_command=True)
    def main(ctx: Context,
             gui_flag: bool = typer.Option(False, "--gui", "-g", help="Starts main game interface in graphical mode")):
        if ctx.invoked_subcommand is None:
            GameManager(INTERFACES[gui_flag]).start()

    @app.command(name='x-pedition', help='this is game x-pedition')
    def x_pedition_app():
        x_pedition.Xpedition(CliUI).start()

    @app.command(name='digit-detective', help='this is game digit-detectiven')
    def digit_detective_app():
        print("Hello digit_detective")
        digit_detective.DigitDetective(CliUI).start()

    @app.command(name='calculator', help='this is game calculator')
    def calculator_app():
        print("Hello calculator")
        calculator.Calculator(CliUI).start()

    return app


if __name__ == "__main__":
    game_app()()
