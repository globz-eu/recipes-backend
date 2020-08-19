from datetime import datetime
from decimal import Decimal
from recipes.models import Recipe
from recipes.serializers import RecipeModelSerializer, RecipeSerializer
from recipes.tests.helpers import get_ingredient_amounts, get_recipe_data
from recipes.tests.models.setup import RecipeIngredients


class RecipeModelSerializerTest(RecipeIngredients):
    def test_serializer(self):
        recipe_data = get_recipe_data('lekker')
        recipe = Recipe.objects.get(pk=self.lekker.pk)
        serializer = RecipeModelSerializer(recipe)
        self.assertEqual(serializer.data['id'], recipe.pk)
        for name, value in recipe_data['recipe'].items():
            self.assertEqual(
                serializer.data[name],
                value
            )
        created = datetime.strptime(serializer.data['created'], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.assertEqual(created.date(), recipe.created.date())
        self.assertEqual(created.time(), recipe.created.time())


class RecipeSerializerTest(RecipeIngredients):
    def test_serializer(self):
        recipe_data = get_recipe_data('lekker')
        recipe, ingredient_amounts = Recipe.recipes.get(pk=self.lekker.pk)
        serializer = RecipeSerializer(dict(recipe=recipe, ingredient_amounts=ingredient_amounts))
        self.assertEqual(serializer.data['recipe']['id'], self.lekker.pk)
        self.assertEqual(
            serializer.data['ingredient_amounts'][0]['ingredient']['id'],
            ingredient_amounts[0].ingredient.id
        )
        self.assertEqual(
            serializer.data['ingredient_amounts'][0]['unit']['name'],
            'piece'
        )
        for name, value in recipe_data['recipe'].items():
            self.assertEqual(
                serializer.data['recipe'][name],
                value
            )
        for i, ingredient in enumerate(recipe_data['ingredient_amounts']):
            self.assertEqual(
                serializer.data['ingredient_amounts'][i]['ingredient']['id'],
                ingredient_amounts[i].ingredient.id
            )
            self.assertEqual(
                serializer.data['ingredient_amounts'][i]['unit']['id'],
                ingredient_amounts[i].unit.id
            )
            for name, value in ingredient.items():
                if isinstance(value, dict):
                    for nested_name, nested_value in value.items():
                        self.assertEqual(
                            serializer.data['ingredient_amounts'][i][name][nested_name],
                            nested_value
                        )
                elif isinstance(value, int):
                    self.assertEqual(
                        int(Decimal(serializer.data['ingredient_amounts'][i][name])),
                        value
                    )
                else:
                    self.assertAlmostEqual(
                        serializer.data['ingredient_amounts'][i][name],
                        value
                    )

    def test_data_serializer(self):
        recipe_data = get_recipe_data('frozen_pizza')
        serializer = RecipeSerializer(
            data=recipe_data
        )
        self.assertTrue(serializer.is_valid())
        for name, value in recipe_data['recipe'].items():
            self.assertEqual(
                serializer.validated_data['recipe'][name],
                value
            )
        for i, ingredient in enumerate(recipe_data['ingredient_amounts']):
            for name, value in ingredient.items():
                self.assertEqual(
                    serializer.validated_data['ingredient_amounts'][i][name],
                    value
                )

    def test_serializer_create(self):
        recipe_data = get_recipe_data('frozen_pizza')
        serializer = RecipeSerializer(
            data=recipe_data
        )
        self.assertTrue(serializer.is_valid())
        recipe = serializer.save()
        ingredient_amounts = get_ingredient_amounts(recipe)
        for name, value in recipe_data['recipe'].items():
            self.assertEqual(
                getattr(recipe, name),
                value
            )
        for i, ingredient in enumerate(recipe_data['ingredient_amounts']):
            for name, value in ingredient.items():
                if isinstance(value, dict):
                    for nested_name, nested_value in value.items():
                        self.assertEqual(
                            getattr(getattr(ingredient_amounts[i], name), nested_name),
                            nested_value
                        )
                elif isinstance(value, int):
                    self.assertEqual(getattr(ingredient_amounts[i], name), Decimal(value))
                else:
                    self.assertEqual(getattr(ingredient_amounts[i], name), value)
