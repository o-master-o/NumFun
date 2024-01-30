import random

from games.base import Game


class DigitDetective(Game):
    NAME = "Digit-detective"
    DEFAULT_MAX_VALUE = 100

    def __init__(self, ui):
        super().__init__(ui)
        self.min_num = 1
        self.max_num = 100
        self.target_num = None

    def start(self):
        self.max_num = self._ask_user_for_max_number()
        self.ui.display_message(f"[green] Maximal value has been set to {self.max_num}")
        self.ui.display_message(f"[green]Now Guessing Game! Guess a number between {self.min_num} and {self.max_num}.[/]")

        self.target_num = random.randint(self.min_num, self.max_num)

        while True:
            guess = int(input("Enter your guess: "))
            result = self._check_guess(guess)
            if result == "correct":
                print("Congratulations! You've guessed the number!")
                break
            else:
                print(f"Try guessing {result}.")

    def _ask_user_for_max_number(self):
        while True:
            answer = self.ui.ask_question(f"[yellow]Please provide maximal number bigger than 1 you want to guess, or press Enter to use default maximal value {self.DEFAULT_MAX_VALUE}\n"
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


    def _check_guess(self, guess):
        if guess < self.target_num:
            return "higher"
        elif guess > self.target_num:
            return "lower"
        else:
            return "correct"
