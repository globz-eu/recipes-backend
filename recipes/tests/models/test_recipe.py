from django.test import TestCase
from recipes.models import Recipe, Ingredient, IngredientAmount, Unit


class RecipeTest(TestCase):

    def setUp(self):
        lekker = Recipe.objects.create(name='Lekker', servings=3, instructions='Stir well')
        garlic = Ingredient.objects.create(name='garlic', plural='garlic')
        aubergine = Ingredient.objects.create(name='aubergine', plural='aubergines')
        piece = Unit.objects.create(name='piece')
        lekker.ingredient_amounts.add(aubergine, through_defaults={'unit': piece, 'quantity': 2})
        lekker.ingredient_amounts.add(garlic, through_defaults={'unit': piece, 'quantity': 1})

    def test_db_fields(self):
        expected_ingredients = [
            {'name': 'aubergine', 'quantity': 2, 'unit_name': 'piece'},
            {'name': 'garlic', 'quantity': 1, 'unit_name': 'piece'}
        ]
        lekker = Recipe.objects.get(name='Lekker')
        ingredients = lekker.ingredient_amounts.all()
        self.assertEqual(lekker.instructions, 'Stir well')
        self.assertEqual(lekker.servings, 3)
        for i, ingredient in enumerate(ingredients):
            ingredient_amount = IngredientAmount.objects.get(
                recipe=lekker,
                ingredient=ingredient
            )
            self.assertEqual(ingredient.name, expected_ingredients[i]['name'])
            self.assertEqual(ingredient_amount.quantity, expected_ingredients[i]['quantity'])
            self.assertEqual(ingredient_amount.unit.name, expected_ingredients[i]['unit_name'])
