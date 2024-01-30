import random

from games.base import Game
from ui.cli_ui import CliUI


class NumberGuessingGame:
    def __init__(self, min_num, max_num):
        self.min_num = min_num
        self.max_num = max_num
        self.target_num = random.randint(min_num, max_num)

    def check_guess(self, guess):
        if guess < self.target_num:
            return "higher"
        elif guess > self.target_num:
            return "lower"
        else:
            return "correct"


class DigitDetective(Game):
    NAME = "Digit-detective"

    def start(self):
        game = NumberGuessingGame(1, 100)
        print(f"Welcome to the Number Guessing Game! Guess a number between {game.min_num} and {game.max_num}.")

        while True:
            guess = int(input("Enter your guess: "))
            result = game.check_guess(guess)
            if result == "correct":
                print("Congratulations! You've guessed the number!")
                break
            else:
                print(f"Try guessing {result}.")
