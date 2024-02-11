from num_fun.games.base import Game
from simpleeval import simple_eval, NameNotDefined, InvalidExpression

from num_fun.games.utils import repeat_endlessly


class Calculator(Game):
    NAME = "Calculator"

    @repeat_endlessly
    def start(self):
        self._play()

    def _play(self):
        answer = ''
        expression = self.ui.ask_question("[green]Enter math expression: [/]")
        try:
            answer = simple_eval(expression)
        except (NameError, NameNotDefined, InvalidExpression, SyntaxError):
            self.ui.display_message("[bold red]Expression is not correct[/]\n")
            return
        self.ui.display_message(f"[{self.ui.LIGHT_YELLOW}]The answer is: {answer}\n")
