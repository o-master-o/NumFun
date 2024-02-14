from unittest.mock import mock_open

import pytest

from num_fun.games.utils import get_game_info

sample_yaml_content = """
game1:
  name: "Game One"
  description: "Description of Game One"
unknown-game:
  name: "Unknown Game"
  description: "This game is not known"
"""


@pytest.fixture
def mock_yaml_data(mocker):
    mocker.patch('builtins.open', mock_open(read_data=sample_yaml_content))
    mocker.patch('yaml.safe_load', return_value={
        'game1': {'name': 'Game One', 'description': 'Description of Game One'},
        'unknown-game': {'name': 'Unknown Game', 'description': 'This game is not known'}
    })


def test_get_game_info_exists(mock_yaml_data):
    info = get_game_info('game1')
    assert info == {'name': 'Game One', 'description': 'Description of Game One'}


def test_get_game_info_not_exists(mock_yaml_data):
    info = get_game_info('nonexistent_game')
    assert info == {'name': 'Unknown Game', 'description': 'This game is not known'}
