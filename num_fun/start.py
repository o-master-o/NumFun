import typer
from typer import Context

from num_fun.games.manager import GameManager
from num_fun.ui.cli_ui import CliUI
from num_fun.ui.gui import GUI
from num_fun.utils import update_git_repo


class NumFun:

    INTERFACES = {True: GUI, False: CliUI}

    def game_app(self):
        app = typer.Typer(
            rich_markup_mode='rich',
            name='num-fun',
            help=CliUI.get_numfun_console_man(),
            context_settings={"help_option_names": ["-h", "--help"]}
        )

        @app.callback(invoke_without_command=True)
        def main(ctx: Context, gui_flag: bool = typer.Option(False, "--gui", "-g",
                                                             help="Starts main game interface in graphical mode. Not implemented yet.")):
            if ctx.invoked_subcommand is None:
                GameManager(self.INTERFACES[gui_flag]).start()

        @app.command(name='update', short_help='Update application')
        def update():
            update_git_repo()

        return app


if __name__ == "__main__":
    NumFun().game_app()()
