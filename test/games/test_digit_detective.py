from unittest.mock import call

import pytest

from num_fun.games.digit_detective import DigitDetective

COMMON_MAX_NUMBER = '15'

CORRECT_ANSWER = 9


@pytest.fixture
def expected_calls(ui):
    def _assert_result(expected_answers):
        answers = {
            'bigger': call(f"[{ui.LIGHT_YELLOW}]Target number is bigger ▲"),
            'smaller': call(f"[{ui.LIGHT_YELLOW}]Target number is smaller ▼"),
        }
        return [answers[answer] for answer in expected_answers]

    return _assert_result


@pytest.fixture
def random(mocker):
    random_mock = mocker.patch("num_fun.games.digit_detective.random")
    random_mock.randint.return_value = CORRECT_ANSWER
    return random_mock


@pytest.mark.parametrize('max_number', ["-5", "-1", "0", "1"])
def test_digit_detective_when_set_incorrect_max_number_user_should_be_shown_warning(ui, max_number):
    ui.ask_question.side_effect = [max_number, KeyboardInterrupt("Exit loop")]

    with pytest.raises(KeyboardInterrupt, match="Exit loop"):
        DigitDetective(ui).start()

    user_warning_message = ui.display_message.mock_calls[0]
    assert call('[bold red] Value should be integer number, and bigger than 1') == user_warning_message


@pytest.mark.parametrize('max_number, expected_max_number', [
    ("", 100),
    ("2", 2),
    ("45", 45),
    ("99", 99),
    ("100", 100),
    ("101", 101),
    ("2345", 2345),
])
def test_digit_detective_set_max_number_correctly(ui, max_number, expected_max_number):
    ui.ask_question.side_effect = [max_number, KeyboardInterrupt("Exit loop")]

    with pytest.raises(KeyboardInterrupt, match="Exit loop"):
        DigitDetective(ui).start()

    max_number_message = ui.display_message.mock_calls[0]
    question_message = ui.display_message.mock_calls[1]
    assert call(f'[green]Maximal value has been set to {expected_max_number}\n') == max_number_message
    assert call(f'[green]Now playing game!\n Guess a number between 1 and {expected_max_number}[/]') == question_message


def test_digit_detective_user_solve_expressions_correctly_in_attempts(ui, expected_calls, random,
                                                                      # user_answers, expected_ui_results
                                                                      ):
    user_answers = [1, 3, 15, 6, 13, 8, 10, CORRECT_ANSWER]
    expected_ui_responses = ['bigger', 'bigger', 'smaller', 'bigger', 'smaller', 'bigger', 'smaller']
    ui.ask_question.side_effect = [COMMON_MAX_NUMBER] + user_answers + [KeyboardInterrupt("Exit loop")]

    with pytest.raises(KeyboardInterrupt, match="Exit loop"):
        DigitDetective(ui).start()

    attempts_result = ui.display_message.mock_calls[2:-1]
    congratulations = ui.display_message.mock_calls[-1]
    assert expected_calls(expected_ui_responses) == attempts_result
    assert call("\n[blink]🌟[not blink] [bold yellow]Congratulations[not bold] [blink]🌟[not blink] You've guessed the number!\n") == congratulations
