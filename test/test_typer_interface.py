import pytest
from typer.testing import CliRunner
from num_fun.ui.cli_ui import CliUI
from num_fun.ui.gui import GUI
from num_fun.start import NumFun


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture
def update_git_repo(mocker):
    return mocker.patch('num_fun.start.update_git_repo')


@pytest.fixture
def game_manager(mocker):
    return mocker.patch('num_fun.start.GameManager')


def test_typer_app_executed_without_arguments_starts_game_manager_with_cli_ui(cli_runner, game_manager):
    result = cli_runner.invoke(NumFun().game_app(), catch_exceptions=False)
    assert result.exit_code == 0
    game_manager.assert_called_once_with(CliUI)
    game_manager.return_value.start.assert_called_once()


def test_typer_app_executed_with_sub_cmd_update_starts_game_update(cli_runner, update_git_repo):
    result = cli_runner.invoke(NumFun().game_app(), ['update'], catch_exceptions=False)
    assert result.exit_code == 0
    update_git_repo.assert_called_once()
    # update_git_repo.assert_called_once_with()


@pytest.mark.parametrize('gui_flag', [
    "--gui",
    "-g",
])
def test_typer_app_executed_with_gui_flag_starts_game_manager_with_gui_ui(cli_runner, game_manager, gui_flag):
    result = cli_runner.invoke(NumFun().game_app(), [gui_flag], catch_exceptions=False)
    assert result.exit_code == 0
    game_manager.assert_called_once_with(GUI)
    game_manager.return_value.start.assert_called_once()
