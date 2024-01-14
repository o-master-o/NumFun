import typer


def game_app():

    app = typer.Typer()

    @app.command()
    def x_pedition():
        print(f"Hello x_pedition")

    @app.command()
    def digit_detective():
        print(f"Hello digit_detective")

    return app


if __name__ == "__main__":
    game_app()()
