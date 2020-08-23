from datetime import datetime
from django.test import TestCase
from recipes.models import Recipe, IngredientAmount
from recipes.tests.helpers import get_recipe_data
from recipes.tests.models.setup import RecipeIngredients


class RecipeTest(RecipeIngredients):

    def test_db_fields(self):
        recipe_data = get_recipe_data('lekker')
        for name, value in recipe_data['recipe'].items():
            self.assertEqual(
                getattr(self.lekker, name),
                value
            )
        self.assertIsInstance(self.lekker.created, datetime)


class RecipeCreateTest(TestCase):

    def test_recipe_create(self):
        recipe_data = get_recipe_data('lekker')
        recipe = Recipe.recipes.create(**recipe_data)
        for name, value in recipe_data['recipe'].items():
            self.assertEqual(
                getattr(recipe, name),
                value
            )
        ingredient_set = recipe.ingredient_set.all()
        for i, ingredient in enumerate(recipe_data['ingredients']):
            for name, value in ingredient['ingredient'].items():
                self.assertEqual(getattr(ingredient_set[i], name), value)
            ingredient_amount = IngredientAmount.objects.select_related('amount').get(
                recipe=recipe,
                ingredient=ingredient_set[i]
            )
            self.assertEqual(
                ingredient_amount.amount.unit.name,
                ingredient['amount']['unit']['name']
            )
            self.assertEqual(ingredient_amount.amount.quantity, ingredient['amount']['quantity'])


class RecipeGetTest(RecipeIngredients):

    def test_recipe_get(self):
        recipe_data = get_recipe_data('lekker')
        recipe, ingredients = Recipe.recipes.get(pk=self.lekker.pk)
        for name, value in recipe_data['recipe'].items():
            self.assertEqual(
                getattr(recipe, name),
                value
            )
        for i, ingredient in enumerate(recipe_data['ingredients']):
            for name, value in ingredient['ingredient'].items():
                self.assertEqual(getattr(ingredients[i].ingredient, name), value)
            self.assertEqual(ingredients[i].amount.unit.name, ingredient['amount']['unit']['name'])
            self.assertEqual(ingredients[i].amount.quantity, ingredient['amount']['quantity'])
