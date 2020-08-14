from django.test import TestCase
from recipes.models import Recipe, Ingredient, Unit


class RecipeIngredients(TestCase):

    def setUp(self):
        self.lekker = Recipe.objects.create(name='Lekker', servings=3, instructions='Stir well')
        self.garlic = Ingredient.objects.create(name='garlic', plural='garlic')
        self.aubergine = Ingredient.objects.create(name='aubergine', plural='aubergines')
        piece = Unit.objects.create(name='piece')
        self.lekker.ingredient_amounts.add(
            self.aubergine,
            through_defaults={'unit': piece, 'quantity': 2}
        )
        self.lekker.ingredient_amounts.add(
            self.garlic,
            through_defaults={'unit': piece, 'quantity': 1}
        )
