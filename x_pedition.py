import random
import os
import emoji


class ExpressionGenerator:
    """Generates algebraic expressions."""

    def __init__(self, max_number):
        self.max_number = max_number

    def generate(self):
        """Generate a simple algebraic expression to solve for x."""
        result = random.randint(1, self.max_number)
        a = random.randint(1, result)
        b = result - a
        x = random.choice([a, b, result])

        if x == a:
            return f"x + {b} = {a + b}", x
        elif x == b:
            return f"{a} + x = {a + b}", x
        else:
            return f"{a} + {b} = x", x


class GameUI:
    """Handles all the User Interface operations for the game."""

    @staticmethod
    def clear_screen():
        """Clear the screen."""
        os.system('clear' if os.name == 'posix' else 'cls')

    @staticmethod
    def display_message(message):
        """Display a message to the user."""
        print(message)

    @staticmethod
    def display_input_message(message):
        """Display an input message and return the user's input."""
        return input(message)

    @staticmethod
    def display_emoji(emoji_code):
        """Display an emoji."""
        print(emoji.emojize(emoji_code))


class Game:
    """Manages the game logic."""

    def __init__(self, max_number, ui):
        self.max_number = max_number
        self.chances = 3
        self.generator = ExpressionGenerator(max_number)
        self.ui = ui

    def start(self):
        """Start the game."""
        try:
            while True:
                expression, answer = self.generator.generate()
                self.ui.display_message('=======================')
                self.ui.display_message("Find x:\n" + expression)

                solved = self.attempt_solve(answer)

                if not solved:
                    self.ui.display_message(f"The correct answer was: {answer}")

                if not self.prompt_continue():
                    break

        except KeyboardInterrupt:
            self.ui.display_message("\nGame exited.")
        except ValueError:
            self.ui.display_message("Invalid input. Please enter a valid number.")

    def attempt_solve(self, answer):
        """Attempt to solve the expression."""
        for _ in range(self.chances):
            user_answer = int(self.ui.display_input_message("Enter the value of x: "))
            if user_answer == answer:
                self.ui.display_emoji(":smiling_cat_with_heart-eyes: Congratulations!")
                return True
            else:
                self.ui.display_emoji(":crying_cat: Try again!")
        return False

    def prompt_continue(self):
        """Prompt the user to continue or exit."""
        user_input = self.ui.display_input_message("Press Enter to continue or type 'exit' and press Enter to exit: ")
        return user_input.strip().lower() != 'exit'


def main():
    GameUI.clear_screen()
    GameUI.display_message('== SKLADATOR ==\nWelcome to the game\n')
    max_number = int(GameUI.display_input_message("Enter the maximum number: "))
    game = Game(max_number, GameUI)
    game.start()


if __name__ == "__main__":
    main()
