import pytest

from num_fun.games.manager import GameManager
from num_fun.ui.cli_ui import CliUI


@pytest.fixture
def prompt(mocker):
    _prompt = mocker.patch('num_fun.ui.cli_ui.prompt')
    _prompt.side_effect = ['X-pedition', KeyboardInterrupt("Exit loop")]
    return _prompt


@pytest.fixture
def xpedition(mocker):
    _game = mocker.patch('num_fun.start.Xpedition')
    _game.NAME = "X-pedition"
    _game.return_value.start.side_effect = [KeyboardInterrupt("Exit loop")]
    return _game


@pytest.fixture
def digit_detective(mocker):
    return mocker.patch('num_fun.start.DigitDetective')


@pytest.fixture
def calculator(mocker):
    return mocker.patch('num_fun.start.Calculator')


@pytest.fixture
def sut(prompt, xpedition, digit_detective, calculator):
    return GameManager(CliUI, [xpedition, digit_detective, calculator])


def test_game_manager_starts_chosen_game(sut, xpedition, digit_detective, calculator):
    sut.start()

    xpedition.return_value.start.assert_called_once()
    digit_detective.return_value.start.assert_not_called()
    calculator.return_value.start.assert_not_called()
