from pathlib import Path

import yaml

INFO_YAML_PATH = Path(__file__).resolve().parent / "info.yaml"


def get_game_info(game_name):
    with open(INFO_YAML_PATH, 'r') as file:
        data = yaml.safe_load(file)
        return data.get(game_name, data['unknown-game'])