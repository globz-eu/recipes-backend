from django.test import TestCase
from recipes.models import Recipe, Ingredient, Unit


class RecipeIngredients(TestCase):

    def setUp(self):
        lekker = Recipe.objects.create(name='Lekker', servings=3, instructions='Stir well')
        garlic = Ingredient.objects.create(name='garlic', plural='garlic')
        aubergine = Ingredient.objects.create(name='aubergine', plural='aubergines')
        piece = Unit.objects.create(name='piece')
        lekker.ingredient_amounts.add(aubergine, through_defaults={'unit': piece, 'quantity': 2})
        lekker.ingredient_amounts.add(garlic, through_defaults={'unit': piece, 'quantity': 1})
