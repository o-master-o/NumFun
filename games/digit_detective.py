import random


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


class GameInterface:
    def __init__(self, game):
        self.game = game

    def start(self):
        print(f"Welcome to the Number Guessing Game! Guess a number between {self.game.min_num} and {self.game.max_num}.")

        while True:
            guess = int(input("Enter your guess: "))
            result = self.game.check_guess(guess)
            if result == "correct":
                print("Congratulations! You've guessed the number!")
                break
            else:
                print(f"Try guessing {result}.")


def detect():
    game = NumberGuessingGame(1, 100)
    interface = GameInterface(game)
    interface.start()


if __name__ == "__main__":
    detect()
