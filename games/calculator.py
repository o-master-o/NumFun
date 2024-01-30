from games.base import Game


class Calculator(Game):
    NAME = "Calculator"

    def start(self):
        while True:
            max_limit = input('Enter expression\n')
            print(eval(max_limit))
