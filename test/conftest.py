import pytest


@pytest.fixture
def ui(mocker):
    ui = mocker.Mock()
    return ui
