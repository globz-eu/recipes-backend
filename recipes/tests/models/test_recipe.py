from django.test import TestCase
from recipes.models import Recipe
from recipes.tests.helpers import get_ingredient_amounts
from recipes.tests.models.setup import RecipeIngredients


class RecipeTest(RecipeIngredients):

    def test_db_fields(self):
        expected_ingredients = ['aubergine', 'garlic']
        lekker = Recipe.objects.get(name='Lekker')
        ingredients = lekker.ingredient_amounts.all()
        self.assertEqual(lekker.name, 'Lekker')
        self.assertEqual(lekker.instructions, 'Stir well')
        self.assertEqual(lekker.servings, 3)
        for i, ingredient in enumerate(ingredients):
            self.assertEqual(ingredient.name, expected_ingredients[i])


class RecipeCreateTest(TestCase):
    def test_recipe_create(self):
        recipe_data = {
            'recipe': {
                'name': 'Lekker',
                'servings': 3,
                'instructions': 'Stir well'
            },
            'ingredient_amounts': [
                {
                    'ingredient': {
                        'name': 'aubergine',
                        'plural': 'aubergines'
                    },
                    'unit': {
                        'name': 'piece'
                    },
                    'quantity': 2
                },
                {
                    'ingredient': {
                        'name': 'garlic',
                        'plural': 'garlic'
                    },
                    'unit': {
                        'name': 'piece'
                    },
                    'quantity': 1
                }
            ]
        }
        recipe = Recipe.recipes.create(**recipe_data)
        self.assertEqual(recipe.name, recipe_data['recipe']['name'])
        self.assertEqual(recipe.servings, recipe_data['recipe']['servings'])
        self.assertEqual(recipe.instructions, recipe_data['recipe']['instructions'])
        ingredient_amounts = get_ingredient_amounts(recipe)
        self.assertEqual(
            ingredient_amounts[0].ingredient.name,
            recipe_data['ingredient_amounts'][0]['ingredient']['name']
        )
        self.assertEqual(
            ingredient_amounts[0].unit.name,
            recipe_data['ingredient_amounts'][0]['unit']['name']
        )
        self.assertEqual(
            ingredient_amounts[0].quantity,
            recipe_data['ingredient_amounts'][0]['quantity']
        )
