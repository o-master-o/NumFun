import random
from enum import Enum

from games.base import Game


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


class Xpedition(Game):
    NAME = "X-pedition"
    DEFAULT_MAX_VALUE = 20

    def __init__(self, ui, chances=3):
        super().__init__(ui)

        self.chances = chances
        self.operations = OPERATIONS.values_list()
        self.generator = ExpressionGenerator()

    def start(self):
        self.generator.max_number = self._ask_user_for_max_number()
        self.ui.display_message(f'[green]Maximal number was set to {self.generator.max_number}\n')
        self.operations = self._ask_user_for_possible_operations_in_expressions()
        self.ui.display_message(f"[green]Operations '{self.generator.max_number}' would be used\n")

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

    # def _set_game_max_number(self):
    #     answer = self.ui.ask_question("Enter the maximum number you want to solve. It should be not bigger than 1000: ")
    #     self.generator.max_number = (int(answer) if answer else 20)
    #     self.ui.display_message(f'Maximal number {self.generator.max_number} was set')

    def _ask_user_for_possible_operations_in_expressions(self):
        question = (f"[yellow]Now You have to choose operations among [b]\'{', '.join(OPERATIONS.values_list())}\'[not b] you want to use\n"
                    f"For example for input [b]+*[not b] will be used expressions with operators [b]+*[not b] (addition and multiplication)\n"
                    f"Please provide it, or press Enter to use all operations in expressions: \'{''.join(OPERATIONS.values_list())}'\n"
                    f"[dim]Enter your answer: ")
        while True:
            answer = self.ui.ask_question(question)
            operations = self._evaluate_chosen_operations(answer)
            if operations:
                return operations

    def _ask_user_for_max_number(self):
        question = (f"[yellow]Now we should choose maximal number you want to solve.\n"
                    f"Number should be positive and bigger or equal to {self.DEFAULT_MAX_VALUE}\n"
                    f"Please provide it, or press Enter to use default value {self.DEFAULT_MAX_VALUE}\n"
                    f"[dim]Your answer: [/]")
        while True:
            answer = self.ui.ask_question(question)
            max_number = self._evaluate_max_value(answer)
            if max_number:
                return max_number

    def _evaluate_max_value(self, value):
        if not value:
            return self.DEFAULT_MAX_VALUE
        try:
            max_int_num = int(value)
            if max_int_num < self.DEFAULT_MAX_VALUE:
                raise ValueError
            return max_int_num
        except ValueError:
            self.ui.display_message(f"[bold red] Value should be integer number, and bigger than or equal to {self.DEFAULT_MAX_VALUE}\n")

    def _evaluate_chosen_operations(self, value):
        if not value:
            return OPERATIONS.values_list()
        try:
            user_operations = set(value)
            for i in user_operations:
                if i not in self.operations:
                    raise ValueError
            return list(user_operations)
        except ValueError:
            self.ui.display_message(f"[bold red] Operations should be in list of operations: \'{''.join(OPERATIONS.values_list())}\'\n")

