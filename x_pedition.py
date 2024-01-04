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

    def __init__(self, max_number):
        self.max_number = min(1000, max(1, max_number))

    def generate_sum(self):
        result = random.randint(1, self.max_number)
        a = random.randint(0, result)
        b = result - a

        return self._prepare_expression(OPERATIONS.ADDITION.value, a, b, result)

    def generate_subtraction(self):
        a = random.randint(1, self.max_number)
        b = random.randint(0, a)
        result = a - b

        return self._prepare_expression(OPERATIONS.SUBTRACTION.value, a, b, result)

    def generate_multiplication(self):
        a = random.randint(1, self.max_number)
        b = random.randint(1, self.max_number // a)  # Ensure that a * b does not exceed max_number
        result = a * b

        return self._prepare_expression(OPERATIONS.MULTIPLICATION.value, a, b, result)

    def generate_division(self):
        result = random.randint(1, self.max_number)
        b = random.randint(1, self.max_number // result)  # Ensure b is a divisor of the result
        a = result * b  # a is now guaranteed to be divisible by b

        return self._prepare_expression(OPERATIONS.DIVISION.value, a, b, result)

    def _prepare_expression(self, operation, a, b, result):
        x_position = random.choice(['a', 'b', 'result'])

        if x_position == 'a':
            return f"x {operation} {b} = {result}", a
        elif x_position == 'b':
            return f"{a} {operation} x = {result}", b
        else:
            return f"{a} {operation} {b} = x", result


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

    def __init__(self, max_number, ui):
        self.max_number = max_number
        self.chances = 3
        self.generator = ExpressionGenerator(max_number)
        self.ui = ui

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


def main():
    ui = CliUI()
    ui.reset_screen()
    ui.display_message('== X-pedition ==\n'
                       'Welcome to the game\n')
    max_number = int(ui.ask_question("Enter the maximum number you want to solve: "))
    game = Game(max_number, ui)
    game.start()


if __name__ == "__main__":
    main()
