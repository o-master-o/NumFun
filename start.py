#!/home/yoda/work/python_projects/NumFun/venv/bin/python
import typer
from rich.console import Console
from rich.panel import Panel

console = Console()


HEADER = """[blue] \n
[yellow]
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                   ┃
┃   ███╗   ██╗██╗   ██╗███╗   ███╗    ███████╗██╗   ██╗███╗   ██╗   ┃
┃   ████╗  ██║██║   ██║████╗ ████║    ██╔════╝██║   ██║████╗  ██║   ┃
┃   ██╔██╗ ██║██║   ██║██╔████╔██║    █████╗  ██║   ██║██╔██╗ ██║   ┃
┃   ██║╚██╗██║██║   ██║██║╚██╔╝██║    ██╔══╝  ██║   ██║██║╚██╗██║   ┃
┃   ██║ ╚████║╚██████╔╝██║ ╚═╝ ██║    ██║     ╚██████╔╝██║ ╚████║   ┃
┃   ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝    ╚═╝      ╚═════╝ ╚═╝  ╚═══╝   ┃
┃                                                                   ┃
┃   ═══════════ Welcome to NumFun! Let's Enjoy Math! ════════════   ┃
┃                                                                   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""


def game_app():

    app = typer.Typer(
        no_args_is_help=True,
        rich_markup_mode='rich',
        name='num-fun',
        help=HEADER,
    )

    @app.command(help='this is game x-pedition')
    def x_pedition():
        print(f"Hello x_pedition")

    @app.command()
    def digit_detective(help='this is game digit-detectiven'):
        print(f"Hello digit_detective")

    @app.command()
    def calculator(help='this is game calculator'):
        print(f"Hello calculator")

    return app


if __name__ == "__main__":
    game_app()()
