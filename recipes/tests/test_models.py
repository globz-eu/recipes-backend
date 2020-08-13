from django.test import TestCase
from ..models import Recipe, Ingredient


class RecipeTest(TestCase):

    def setUp(self):
        lekker = Recipe.objects.create(name='Lekker', servings=3, instructions='Stir well')
        garlic = Ingredient.objects.create(name='garlic', plural='garlic')
        aubergine = Ingredient.objects.create(name='aubergine', plural='aubergines')
        aubergine.recipes.add(lekker)
        garlic.recipes.add(lekker)

    def test_db_fields(self):
        lekker = Recipe.objects.get(name='Lekker')
        self.assertEqual(lekker.instructions, 'Stir well')
        self.assertEqual(lekker.servings, 3)
        self.assertEqual(
            [ingredient.name for ingredient in lekker.ingredient_set.all()],
            ['aubergine', 'garlic']
        )


class IngredientTest(TestCase):

    def setUp(self):
        lekker = Recipe.objects.create(name='Lekker', servings=3, instructions='Stir well')
        garlic = Ingredient.objects.create(name='garlic', plural='garlic')
        aubergine = Ingredient.objects.create(name='aubergine', plural='aubergines')
        aubergine.recipes.add(lekker)
        garlic.recipes.add(lekker)

    def test_db_fields(self):
        aubergine = Ingredient.objects.get(name='aubergine')
        self.assertEqual(aubergine.plural, 'aubergines')
        self.assertEqual(aubergine.recipes.first().name, 'Lekker')
