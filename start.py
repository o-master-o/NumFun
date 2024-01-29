#!/home/yoda/work/python_projects/NumFun/venv/bin/python
import typer
from rich.console import Console
from typer import Context

from games import x_pedition, digit_detective, calculator
from ui import gui, cli_ui
from utils import HEADER

console = Console()


def game_app():

    app = typer.Typer(
        rich_markup_mode='rich',
        name='num-fun',
        help=HEADER,
    )

    @app.callback(invoke_without_command=True)
    def main(ctx: Context,
             gui_flag: bool = typer.Option(False, "--gui", "-g", help="Starts main game interface in graphical mode")):
        if ctx.invoked_subcommand is None:
            if gui_flag:
                gui.start_main_game_interface()
            else:
                cli_ui.start_main_game_interface()

    @app.command(name='x-perdition', help='this is game x-pedition')
    def x_pedition_app():
        x_pedition.main()

    @app.command(name='digit-detective', help='this is game digit-detectiven')
    def digit_detective_app():
        print("Hello digit_detective")
        digit_detective.main()

    @app.command(name='calculator', help='this is game calculator')
    def calculator_app():
        print("Hello calculator")
        calculator.main()

    return app


if __name__ == "__main__":
    game_app()()
