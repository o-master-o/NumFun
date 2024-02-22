import pytest

from num_fun.games.calculator import Calculator, simple_eval


@pytest.fixture
def assert_result(ui):
    def _assert_result(expected_result):
        ui.display_message.assert_called_with(f"[{ui.LIGHT_YELLOW}]The answer is: {expected_result}\n")
    return _assert_result


@pytest.mark.parametrize('expression_string, expected_result', [
    ("2+3", 5),
    ("5-3", 2),
    ("8/2", 4.0),
    ("6*2", 12),
    ("(5-2+11)/2", 7.0),
    ("5-2+11", 14),
])
def test_calculator_solve_expressions_correctly(ui, assert_result, expression_string, expected_result):
    ui.ask_question.side_effect = [expression_string, KeyboardInterrupt("Exit loop")]

    with pytest.raises(KeyboardInterrupt, match="Exit loop"):
        Calculator(ui).start()

    ui.ask_question.assert_called_with("[green]Enter math expression: [/]")
    assert_result(expected_result)


def test_calculator_invalid_expression(ui, mocker):
    ui.ask_question.side_effect = ["invalid expression", KeyboardInterrupt("Exit loop")]

    with pytest.raises(KeyboardInterrupt, match="Exit loop"):
        Calculator(ui).start()
    ui.display_message.assert_called_with("[bold red]Expression is not correct[/]\n")
