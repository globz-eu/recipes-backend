import json
from pathlib import Path, PurePath


def get_recipe_data(name):
    recipe_data_file = Path(
        PurePath(
            Path(__file__).cwd()
        ).joinpath(
            f'recipes/tests/data/{name}.json'
        )
    )
    return json.load(recipe_data_file.open())
