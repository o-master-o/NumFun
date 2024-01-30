from games.base import Game
from games.utils import CALCULATOR_HEADER


class Calculator(Game):
    NAME = "Calculator"
    HEADER = CALCULATOR_HEADER

    def start(self):
        while True:
            max_limit = input('Enter expression\n')
            print(eval(max_limit))


def main():
    Calculator().start()


if __name__ == "__main__":
    main()
