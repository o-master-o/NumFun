import pytest

from num_fun.games.manager import GameManager, GamesPocket
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
    _game = mocker.patch('num_fun.start.DigitDetective')
    _game.NAME = "Digit-detective"
    return _game


@pytest.fixture
def calculator(mocker):
    _game = mocker.patch('num_fun.start.Calculator')
    _game.NAME = "Calculator"
    return _game


@pytest.fixture
def manager_sut(prompt, xpedition, digit_detective, calculator):
    return GameManager(CliUI, [xpedition, digit_detective, calculator])


def test_game_manager_starts_chosen_game(manager_sut, xpedition, digit_detective, calculator):
    manager_sut.start()

    xpedition.return_value.start.assert_called_once()
    digit_detective.return_value.start.assert_not_called()
    calculator.return_value.start.assert_not_called()


@pytest.mark.parametrize('game_mame', [
    "X-pedition",
    "Calculator",
    "Digit-detective"
])
def test_games_pocket_returns_chosen_game_if_exists(xpedition, digit_detective, calculator, game_mame):
    pocket = GamesPocket([xpedition, digit_detective, calculator])
    game = pocket.get(game_mame)
    assert game_mame == game.NAME


def test_games_pocket_returns_none_if_game_is_nonexistent(xpedition, digit_detective, calculator):
    pocket = GamesPocket([xpedition, digit_detective, calculator])
    game = pocket.get('nonexistent-game-mame')
    assert game is None


def test_games_pocket_returns_all_games_names_list(xpedition, digit_detective, calculator):
    pocket = GamesPocket([xpedition, digit_detective, calculator])
    assert ['X-pedition', 'Digit-detective', 'Calculator'] == pocket.names
