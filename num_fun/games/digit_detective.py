import random

from num_fun.games.base import Game
from num_fun.games.utils import repeat_endlessly


class DigitDetective(Game):
    NAME = "Digit-detective"
    DEFAULT_MAX_VALUE = 100

    def __init__(self, ui):
        super().__init__(ui)
        self.min_num = 1
        self.max_num = 100
        self.target_num = None

    @repeat_endlessly
    def start(self):
        self._play()

    def _play(self):
        self._generate_number()
        self._gues_number()

    def _gues_number(self):
        self.ui.display_message(f"[green]Now playing game!\n Guess a number between {self.min_num} and {self.max_num}[/]")
        while True:
            user_guess = self._ask_user_to_guess_number()
            result = self._check_guess(user_guess)
            if result == "correct":
                self.ui.display_message(f"\n[blink]🌟[not blink] [bold yellow]Congratulations[not bold] [blink]🌟[not blink] "
                                        f"You've guessed the number!\n")
                break
            else:
                self.ui.display_message(f"[{self.ui.LIGHT_YELLOW}]Target number is {result}")

    def _generate_number(self):
        self.max_num = self._ask_user_for_max_number()
        self.ui.display_message(f"[green]Maximal value has been set to {self.max_num}\n")
        self.target_num = random.randint(self.min_num, self.max_num)

    def _ask_user_for_max_number(self):
        while True:
            answer = self.ui.ask_question(f"[yellow]Please provide maximal number bigger than 1 you want to guess, "
                                          f"or press Enter to use default maximal value {self.DEFAULT_MAX_VALUE}\n"
                                          f"[dim]Your answer: [/]")
            max_number = self._evaluate_max_value(answer)
            if max_number:
                return max_number

    def _evaluate_max_value(self, value):
        if not value:
            return self.DEFAULT_MAX_VALUE
        try:
            max_int_num = int(value)
            if max_int_num <= 1:
                raise ValueError
            return max_int_num
        except ValueError:
            self.ui.display_message(f"[bold red] Value should be integer number, and bigger than 1")

    def _ask_user_to_guess_number(self):
        while True:
            answer = self.ui.ask_question(f"[{self.ui.LIGHT_YELLOW}]Enter your guess: ")
            try:
                return int(answer)
            except ValueError:
                self.ui.display_message(f"[{self.ui.LIGHT_YELLOW}]Incorrect input. Enter your guess: ")
                continue

    def _check_guess(self, guess):
        if guess < self.target_num:
            return "bigger ▲"
        elif guess > self.target_num:
            return "smaller ▼"
        else:
            return "correct"
