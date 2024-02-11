from unittest.mock import call
from collections import Counter

import pytest
from num_fun.games.x_pedition import Xpedition

COMMON_MAX_NUMBER = '15'
INCORRECT_ANSWER = 'some incorrect answer'

SOME_EXPRESSION = 'some expression'
CORRECT_ANSWER = 'some correct answer'

ANOTHER_EXPRESSION = 'some another expression'
ANOTHER_CORRECT_ANSWER = 'some another correct answer'


@pytest.fixture
def expression_generator(mocker):
    generator = mocker.patch('num_fun.games.x_pedition.ExpressionGenerator')
    generator.return_value.generate_random_expression.side_effect = [(SOME_EXPRESSION, CORRECT_ANSWER), (ANOTHER_EXPRESSION, CORRECT_ANSWER)]
    return generator


@pytest.fixture
def build_expected_calls(ui):
    def _assert_result(expected_answers):
        answers = {'incorrect': call(ui.COMMISERATIONS),
                   'correct': call(ui.CONGRATULATIONS),
                   'answer is shown': call('The correct answer was: some correct answer\n')}
        return [answers[answer] for answer in expected_answers]

    return _assert_result


@pytest.fixture
def question_with_expression_message_call(ui):
    def _question(expression):
        return call(f"[{ui.LIGHT_YELLOW}]==== Find [b]x[not b] ======================\n"
                    f"  [white][b]{expression}[not b][{ui.LIGHT_YELLOW}]\n"
                    f"==================================\n"
                    f"[white]Enter the value of x: ")
    return _question


@pytest.mark.parametrize('max_number', ["-5", "-1", "0", "5", "9"])
def test_x_pedition_when_set_incorrect_max_number_user_should_be_shown_warning(ui, expression_generator, max_number):
    ui.ask_question.side_effect = [max_number, KeyError("Exit loop")]

    with pytest.raises(KeyError, match="Exit loop"):
        Xpedition(ui).start()

    user_warning_message = ui.display_message.mock_calls[0]
    assert call('[bold red] Value should be integer number, and bigger than or equal to 10\n') == user_warning_message


@pytest.mark.parametrize('max_number, expected_max_number', [
    ("", 10),
    ("10", 10),
    ("11", 11),
    ("100", 100),
])
def test_x_pedition_when_max_number_was_chosen_than_user_should_be_informed_about_value(ui, expression_generator, max_number, expected_max_number):
    ui.ask_question.side_effect = [max_number, KeyError("Exit loop")]

    with pytest.raises(KeyError, match="Exit loop"):
        Xpedition(ui).start()

    max_number_message = ui.display_message.mock_calls[0]
    assert call(f'[green]Maximal number will be set to {expected_max_number}\n') == max_number_message
    assert 2 == ui.ask_question.call_count
    assert 1 == ui.display_message.call_count


@pytest.mark.parametrize("user_operations, expected_operations", [
    ("", ["+", "-", "*", "/"]),
    ("+-", ["+", "-"]),
    ("+*-", ["+", "*", "-"]),
    ("/+*-", ["/", "+", "*", "-"]),
    ("/+*-+++", ["/", "+", "*", "-"]),
])
def test_x_pedition_set_operations_correctly(ui, expression_generator, user_operations, expected_operations):
    ui.ask_question.side_effect = [COMMON_MAX_NUMBER, user_operations, KeyError("Exit loop")]

    with pytest.raises(KeyError, match="Exit loop"):
        Xpedition(ui).start()
    assert Counter(expected_operations) == Counter(expression_generator().generate_random_expression.call_args[0][0])


@pytest.mark.parametrize("user_answers, expected_ui_results", [
    ([CORRECT_ANSWER], ['correct']),
    ([INCORRECT_ANSWER, CORRECT_ANSWER], ['incorrect', 'correct']),
    ([INCORRECT_ANSWER, INCORRECT_ANSWER, CORRECT_ANSWER], ['incorrect', 'incorrect', 'correct']),
    ([INCORRECT_ANSWER, INCORRECT_ANSWER, INCORRECT_ANSWER], ['incorrect', 'incorrect', 'incorrect', 'answer is shown']),
])
def test_x_pedition_user_solve_expressions_correctly_in_attempts(ui, expression_generator, build_expected_calls,
                                                                 question_with_expression_message_call, user_answers, expected_ui_results):
    build_expected_calls(expected_ui_results)
    ui.ask_question.side_effect = [COMMON_MAX_NUMBER, ''] + user_answers + [KeyError("Exit loop")]

    with pytest.raises(KeyError, match="Exit loop"):
        Xpedition(ui).start()

    initial_expression_message_call = ui.display_message.mock_calls[2]
    attempts_result = ui.display_message.mock_calls[3:-1]
    next_iteration_expression_message_call = ui.display_message.mock_calls[-1]

    assert build_expected_calls(expected_ui_results) == attempts_result
    assert question_with_expression_message_call(SOME_EXPRESSION) == initial_expression_message_call
    assert question_with_expression_message_call(ANOTHER_EXPRESSION) == next_iteration_expression_message_call
