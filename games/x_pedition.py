import random
from enum import Enum

from ui.cli_ui import CliUI


class OPERATIONS(Enum):
    ADDITION = '+'
    SUBTRACTION = '-'
    MULTIPLICATION = '*'
    DIVISION = '/'

    @classmethod
    def values_list(cls):
        return [member.value for member in cls]


class ExpressionGenerator:

    def __init__(self):
        self._max_number = 10

    @property
    def max_number(self):
        return self._max_number

    @max_number.setter
    def max_number(self, value):
        self._max_number = min(1000, max(1, value))

    def generate_random_expression(self, operations):
        operation_methods = {
            OPERATIONS.ADDITION.value: self.generate_sum,
            OPERATIONS.SUBTRACTION.value: self.generate_subtraction,
            OPERATIONS.MULTIPLICATION.value: self.generate_multiplication,
            OPERATIONS.DIVISION.value: self.generate_division
        }

        available_methods = [operation_methods[op] for op in operations if op in operation_methods]
        if not available_methods:
            raise ValueError("Invalid or unsupported operations provided.")

        chosen_method = random.choice(available_methods)
        return chosen_method()

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


class XpeditionGame:

    def __init__(self, ui, chances=3):
        self.chances = chances
        self.operations = OPERATIONS.values_list()
        self.ui = ui
        self.generator = ExpressionGenerator()

    def start(self):
        self._prepare()

        try:
            while True:
                expression, answer = self.generator.generate_random_expression(self.operations)
                self.ui.display_message("=======================\nFind x:\n" + expression)
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

    def _prepare(self):
        self.ui.reset_screen()
        self.ui.display_message('== X-pedition ==\nWelcome to the game\n')
        self._set_game_max_number()
        self._set_available_operations()

    def _set_game_max_number(self):
        answer = self.ui.ask_question("Enter the maximum number you want to solve. It should be not bigger than 1000: ")
        self.generator.max_number = (int(answer) if answer else 20)
        self.ui.display_message(f'Maximal number {self.generator.max_number} was set')

    def _set_available_operations(self):
        user_input = self.ui.ask_question("You have to choose operations you want to use\n"
                                          "+) +\n"
                                          "-) -\n"
                                          "*) *\n"
                                          "/) /\n"
                                          "By default all operations will be used '+-*/'"
                                          "For example +* will use +* (addition and multiplication expressions)\n"
                                          "Enter your answer: ")
        self.operations = user_input or OPERATIONS.values_list()


def main():
    game = XpeditionGame(CliUI())
    game.start()


if __name__ == "__main__":
    main()
