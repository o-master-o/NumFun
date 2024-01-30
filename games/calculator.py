from games.base import Game
from simpleeval import simple_eval, NameNotDefined, InvalidExpression


class Calculator(Game):
    NAME = "Calculator"

    def start(self):
        while True:
            answer = ''
            expression = self.ui.ask_question("[green]Enter math expression: [/]")
            try:
                answer = simple_eval(expression)
            except (NameError, NameNotDefined, InvalidExpression, SyntaxError):
                self.ui.display_message("[bold red]Expression is not correct[/]\n")
                continue
            self.ui.display_message(f"The answer is: {answer}\n")