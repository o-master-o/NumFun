import random
import os
from abc import ABC, abstractmethod
from enum import Enum

import emoji


class OPERATIONS(Enum):
    ADDITION = '+'
    SUBTRACTION = '-'
    MULTIPLICATION = '*'
    DIVISION = '/'


class ExpressionGenerator:

    def __init__(self):
        self._max_number = 10

    @property
    def max_number(self):
        return self._max_number

    @max_number.setter
    def max_number(self, value):
        self._max_number = min(1000, max(1, value))

    def generate_sum(self):
        result = random.randint(1, self._max_number)
        a = random.randint(0, result)
        b = result - a

        return self._prepare_expression(OPERATIONS.ADDITION.value, a, b, result)

    def generate_subtraction(self):
        a = random.randint(1, self._max_number)
        b = random.randint(0, a)
        result = a - b

        return self._prepare_expression(OPERATIONS.SUBTRACTION.value, a, b, result)

    def generate_multiplication(self):
        a = random.randint(1, self._max_number)
        b = random.randint(1, self._max_number // a)
        result = a * b

        return self._prepare_expression(OPERATIONS.MULTIPLICATION.value, a, b, result)

    def generate_division(self):
        result = random.randint(1, self._max_number)
        b = random.randint(1, self._max_number // result)
        a = result * b

        return self._prepare_expression(OPERATIONS.DIVISION.value, a, b, result)

    @staticmethod
    def _prepare_expression(operation, a, b, result):
        variables = {'a': a, 'b': b, 'result': result}
        x_position = random.choice(list(variables.keys()))
        x = variables[x_position]
        variables[x_position] = 'x'
        return f"{variables['a']} {operation} {variables['b']} = {variables['result']}", x


class UI(ABC):
    @abstractmethod
    def reset_screen(self):
        pass

    @abstractmethod
    def display_message(self, message):
        pass

    @abstractmethod
    def ask_question(self, message):
        pass


class CliUI(UI):
    CONGRATULATIONS = f"{emoji.emojize(':smiling_cat_with_heart-eyes:')} Congratulations!"
    COMMISERATIONS = f"{emoji.emojize(':crying_cat:')} Try again!"

    def reset_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def display_message(self, message):
        print(message)

    def ask_question(self, message):
        return input(message)


class Game:

    def __init__(self, ui):
        self.chances = 3
        self.ui = ui
        self.generator = ExpressionGenerator()

    def start(self):
        try:
            while True:
                expression, answer = self.generator.generate_sum()
                self.ui.display_message('=======================')
                self.ui.display_message("Find x:\n" + expression)

                solved = self.attempt_solve(answer)

                if not solved:
                    self.ui.display_message(f"The correct answer was: {answer}")

                if not self.prompt_continue():
                    break

        except KeyboardInterrupt:
            self.ui.display_message("\nGame exited.")

    def attempt_solve(self, answer):
        for _ in range(self.chances):
            user_answer = int(self.ui.ask_question("Enter the value of x: "))
            if user_answer == answer:
                self.ui.display_message(self.ui.CONGRATULATIONS)
                return True
            else:
                self.ui.display_message(self.ui.COMMISERATIONS)
        return False

    def prompt_continue(self):
        user_input = self.ui.ask_question("Press Enter to continue or type 'exit' and press Enter to exit: ")
        return user_input.strip().lower() != 'exit'

    def prepare(self):
        self.ui.reset_screen()
        self.ui.display_message('== X-pedition ==\n'
                                'Welcome to the game\n')
        max_number = int(self.ui.ask_question("Enter the maximum number you want to solve: "))
        self.generator.max_number = max_number


def main():
    game = Game(CliUI())
    game.prepare()
    game.start()


if __name__ == "__main__":
    main()
