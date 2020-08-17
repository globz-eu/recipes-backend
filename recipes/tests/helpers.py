import json
from pathlib import Path, PurePath
from recipes.models import Ingredient, IngredientAmount


def get_ingredient_amounts(recipe):
    ingredient_ids = [ingredient.pk for ingredient in recipe.ingredient_amounts.all()]
    ingredients = Ingredient.objects.filter(pk__in=ingredient_ids)
    return IngredientAmount.objects.filter(
        recipe=recipe,
        ingredient__in=ingredients
    )


def get_recipe_data(name):
    recipe_data_file = Path(
        PurePath(
            Path(__file__).cwd()
        ).joinpath(
            f'recipes/tests/data/{name}.json'
        )
    )
    return json.load(recipe_data_file.open())
