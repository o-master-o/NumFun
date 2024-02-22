import random
from enum import Enum

from num_fun.games.base import Game
from num_fun.games.utils import repeat_endlessly


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
        self._max_number = None

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
    DEFAULT_MAX_VALUE = 10

    def __init__(self, ui, chances=3):
        super().__init__(ui)
        self.chances = chances
        self.operations = OPERATIONS.values_list()
        self.generator = ExpressionGenerator()

    def start(self):
        self.generator.max_number = self._ask_user_for_max_number()
        self.operations = self._ask_user_for_possible_operations_in_expressions()
        self._play()

    @repeat_endlessly
    def _play(self):
        expression, answer = self.generator.generate_random_expression(self.operations)
        self.ui.display_message(f"[{self.ui.LIGHT_YELLOW}]==== Find [b]x[not b] ======================\n"
                                f"  [white][b]{expression}[not b][{self.ui.LIGHT_YELLOW}]\n"
                                f"==================================\n"
                                f"[white]Enter the value of x: ")
        solved = self._attempts_to_solve(answer)
        if not solved:
            self.ui.display_message(f"The correct answer was: {answer}\n")
            return

    def _attempts_to_solve(self, answer):
        for attempt_number in range(1, self.chances + 1):
            user_answer = self._get_user_answer(attempt_number)
            if user_answer == answer:
                self.ui.display_message(self.ui.CONGRATULATIONS)
                return True
            else:
                self.ui.display_message(self.ui.COMMISERATIONS)
        return False

    def _ask_user_for_max_number(self):
        question = (f"[yellow]Now we should choose maximal number you want to solve.\n"
                    f"Number should be positive and bigger or equal to {self.DEFAULT_MAX_VALUE}\n"
                    f"Please provide it, or press Enter to use default value {self.DEFAULT_MAX_VALUE}\n"
                    f"[dim]Enter Your answer: [/]")
        while True:
            answer = self.ui.ask_question(question)
            max_number = self._evaluate_max_value(answer)
            if max_number:
                self.ui.display_message(f'[green]Maximal number will be set to {max_number}\n')
                return max_number

    def _ask_user_for_possible_operations_in_expressions(self):
        question = (f"[yellow]Now You have to choose operations among [b]\'{', '.join(OPERATIONS.values_list())}\'[not b] you want to use\n"
                    f"For example for input [b]+*[not b] will be used expressions with operators [b]+*[not b] (addition and multiplication)\n"
                    f"Please provide it, or press Enter to use all operations in expressions: \'{' '.join(OPERATIONS.values_list())}'\n"
                    f"[dim]Enter your answer: ")
        while True:
            answer = self.ui.ask_question(question)
            operations = self._evaluate_chosen_operations(answer)
            if operations:
                self.ui.display_message(f"[green]Operations '{''.join(operations)}' will be used\n")
                return operations

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

    def _get_user_answer(self, attempt_number):
        user_answer = self.ui.ask_question(f"[green]Attempt [b]{attempt_number}[not b]: ")
        try:
            return int(user_answer)
        except ValueError:
            return user_answer
