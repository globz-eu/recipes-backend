from datetime import datetime
from recipes.models import Recipe
from recipes.serializers import RecipeModelSerializer, RecipeSerializer
from recipes.tests.helpers import get_recipe_data, get_recipe_data_flat
from recipes.tests.helpers import get_recipe_no_ingredients, get_ingredient_amounts
from recipes.tests.models.setup import RecipeIngredients


class RecipeModelSerializerTest(RecipeIngredients):
    def test_serializer(self):
        recipe_data = get_recipe_data('lekker')
        recipe = Recipe.objects.get(pk=self.lekker.pk)
        serializer = RecipeModelSerializer(recipe)
        self.assertEqual(serializer.data['id'], recipe.pk)
        self.compare_values(serializer.data, recipe_data['recipe'])
        created = datetime.strptime(serializer.data['created'], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.assertEqual(created.date(), recipe.created.date())
        self.assertEqual(created.time(), recipe.created.time())


class RecipeSerializerTest(RecipeIngredients):
    def test_serializer(self):
        recipe_data = get_recipe_data('lekker')
        recipe, ingredient_amounts = Recipe.recipes.get(pk=self.lekker.pk)
        serializer = RecipeSerializer(dict(recipe=recipe, ingredients=ingredient_amounts))
        self.assertEqual(serializer.data['id'], self.lekker.pk)
        self.compare_values(get_recipe_no_ingredients(serializer.data), recipe_data['recipe'])
        for i, ingredient in enumerate(recipe_data['ingredients']):
            self.compare_values(serializer.data['ingredients'][i], ingredient)
            self.assertEqual(
                serializer.data['ingredients'][i]['ingredient']['id'],
                ingredient_amounts[i].ingredient.id
            )
            self.assertEqual(
                serializer.data['ingredients'][i]['amount']['unit']['id'],
                ingredient_amounts[i].amount.unit.id
            )

    def test_data_serializer(self):
        recipe_data, expected_recipe = get_recipe_data_flat('frozen_pizza')
        serializer = RecipeSerializer(data=recipe_data)
        self.assertTrue(serializer.is_valid())
        serializer_recipe = get_recipe_no_ingredients(serializer.data)
        self.compare_values(serializer_recipe, expected_recipe)
        for i, ingredient in enumerate(recipe_data['ingredients']):
            self.compare_values(serializer.validated_data['ingredients'][i], ingredient)

    def test_serializer_create(self):
        recipe_data, expected_recipe = get_recipe_data_flat('frozen_pizza')
        serializer = RecipeSerializer(data=recipe_data)
        self.assertTrue(serializer.is_valid())
        recipe = serializer.save()
        ingredient_amounts = get_ingredient_amounts(recipe)
        self.compare_object_values(recipe, expected_recipe)
        for i, ingredient in enumerate(recipe_data['ingredients']):
            self.compare_object_values(ingredient_amounts[i], ingredient)

    def test_serializer_update_recipe(self):
        recipe_data, _ = get_recipe_data_flat('lekker')
        recipe_data['instructions'] = "Stir well for 20 minutes"
        recipe, _ = Recipe.recipes.get(pk=self.lekker.pk)
        serializer = RecipeSerializer(recipe, data=recipe_data)
        self.assertTrue(serializer.is_valid())
        recipe = serializer.save()
        self.compare_object_values(recipe, get_recipe_no_ingredients(recipe_data))

    def test_serializer_update_recipe_ingredients(self):
        recipe_data, expected_recipe = get_recipe_data_flat('lekker')
        recipe_data['ingredients'][1]['ingredient']['name'] = "onion"
        recipe_data['ingredients'][1]['ingredient']['plural'] = "onions"
        recipe, _ = Recipe.recipes.get(pk=self.lekker.pk)
        serializer = RecipeSerializer(recipe, data=recipe_data)
        self.assertTrue(serializer.is_valid())
        recipe = serializer.save()
        ingredient_amounts = get_ingredient_amounts(recipe)
        self.compare_object_values(recipe, expected_recipe)
        for i, ingredient in enumerate(recipe_data['ingredients']):
            self.compare_object_values(ingredient_amounts[i], ingredient)
