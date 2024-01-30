from games.base import Game


class Calculator(Game):
    NAME = "Calculator"

    def start(self):
        while True:
            max_limit = input('Enter expression\n')
            print(eval(max_limit))


def main():
    Calculator().start()


if __name__ == "__main__":
    main()
