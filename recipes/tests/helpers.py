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
    recipe = json.load(recipe_data_file.open())
    return {
        'recipe': {key: value for (key, value) in recipe.items() if key != 'ingredients'},
        'ingredients': recipe['ingredients']
    }


def get_ingredient_amounts(recipe):
    return [
        IngredientAmount.objects.select_related('amount').get(
            recipe=recipe,
            ingredient=ingredient
        ) for ingredient in recipe.ingredient_set.all()
    ]


def check_values(returned, expected, assertion, returned_is_object=False):
    for name, value in expected.items():
        if returned_is_object:
            if isinstance(value, dict):
                check_values(getattr(returned, name), value, assertion, returned_is_object=True)
            else:
                assertion(getattr(returned, name), value)
        else:
            if isinstance(value, dict):
                check_values(returned[name], value, assertion)
            else:
                assertion(returned[name], value)
