from django.test import TestCase
from recipes.models import Recipe, Ingredient


class IngredientTest(TestCase):

    def setUp(self):
        lekker = Recipe.objects.create(name='Lekker', servings=3, instructions='Stir well')
        pas_mal = Recipe.objects.create(
            name='Pas mal',
            servings=2,
            instructions='Servir sur un lit de choucroute'
        )
        aubergine = Ingredient.objects.create(name='aubergine', plural='aubergines')
        aubergine.recipes.add(lekker)
        aubergine.recipes.add(pas_mal)

    def test_db_fields(self):
        aubergine = Ingredient.objects.get(name='aubergine')
        self.assertEqual(aubergine.plural, 'aubergines')
        self.assertEqual(aubergine.recipes.first().name, 'Lekker')
        self.assertEqual(aubergine.recipes.all()[1].name, 'Pas mal')
