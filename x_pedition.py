import random
import os
import emoji


def generate_expression(max_number):
    """Generate a simple algebraic expression to solve for x."""
    result = random.randint(1, max_number)
    a = random.randint(1, result)
    b = result - a
    x = random.choice([a, b, result])
    if x == a:
        return f"x + {b} = {a + b}", x
    elif x == b:
        return f"{a} + x = {a + b}", x
    else:
        return f"{a} + {b} = x", x


def play_game():
    """Main function to play the game."""
    os.system('clear')
    print('== SKLADATOR ==\n'
          'Witamy w grze\n')
    try:
        max_number = int(input("Wprowadż maksymalną liczbe: "))
        chances = 3

        while True:
            expression, answer = generate_expression(max_number)
            print('=======================')
            print("Odnajdź x:\n", expression)

            for _ in range(chances):
                user_answer = int(input("Wpisz czym jest x: "))
                if user_answer == answer:
                    print(emoji.emojize(":smiling_cat_with_heart-eyes: WYGRAŁEŚ!"))
                    break
                else:
                    print("")
                    print(emoji.emojize(":crying_cat: Spróbuj znowu!"))
            else:
                print(f"Prawidłowa odpowiedż to: {answer}")

            if input("Wprowadź dowolny znak żeby kontynuować"
                     "Lub Ctrl+C żeby wyjść: "):
                continue

    except KeyboardInterrupt:
        print("\n ====== GAME OVER =======")
    except ValueError:
        print("Nieprawidłowy wpis. Wprowadzaj liczbę")


if __name__ == "__main__":
    play_game()
