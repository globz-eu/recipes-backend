import json
from pathlib import Path, PurePath
from recipes.models import IngredientAmount


def get_recipe_data(name):
    recipe_data_file = Path(
        PurePath(
            Path(__file__).cwd()
        ).joinpath(
            f'recipes/tests/data/{name}.json'
        )
    )
    return json.load(recipe_data_file.open())


def get_ingredient_amounts(recipe):
    return [
        IngredientAmount.objects.select_related('amount').get(
            recipe=recipe,
            ingredient=ingredient
        ) for ingredient in recipe.ingredient_set.all()
    ]
