from datetime import datetime
from decimal import Decimal
from recipes.models import Recipe, IngredientAmount
from recipes.serializers import RecipeModelSerializer, RecipeSerializer
from recipes.tests.helpers import get_recipe_data
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
        serializer = RecipeSerializer(dict(recipe=recipe, ingredients=ingredient_amounts))
        self.assertEqual(serializer.data['recipe']['id'], self.lekker.pk)
        self.assertEqual(
            serializer.data['ingredients'][0]['ingredient']['id'],
            ingredient_amounts[0].ingredient.id
        )
        self.assertEqual(
            serializer.data['ingredients'][0]['amount']['unit']['name'],
            'piece'
        )
        for name, value in recipe_data['recipe'].items():
            self.assertEqual(
                serializer.data['recipe'][name],
                value
            )
        for i, ingredient in enumerate(recipe_data['ingredients']):
            self.assertEqual(
                serializer.data['ingredients'][i]['ingredient']['id'],
                ingredient_amounts[i].ingredient.id
            )
            self.assertEqual(
                serializer.data['ingredients'][i]['amount']['unit']['id'],
                ingredient_amounts[i].amount.unit.id
            )
            for name, value in ingredient.items():
                if isinstance(value, dict):
                    for nested_name, nested_value in value.items():
                        self.assertEqual(
                            serializer.data['ingredients'][i][name][nested_name],
                            nested_value
                        )
                elif isinstance(value, int):
                    self.assertEqual(
                        int(Decimal(serializer.data['ingredients'][i][name])),
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
        for i, ingredient in enumerate(recipe_data['ingredients']):
            for name, value in ingredient.items():
                self.assertEqual(
                    serializer.validated_data['ingredients'][i][name],
                    value
                )

    def test_serializer_create(self):
        recipe_data = get_recipe_data('frozen_pizza')
        serializer = RecipeSerializer(
            data=recipe_data
        )
        self.assertTrue(serializer.is_valid())
        recipe = serializer.save()
        ingredient_set = self.lekker.ingredient_set.all()
        ingredient_amounts = [
            IngredientAmount.objects.select_related('amount').get(
                recipe=self.lekker,
                ingredient=ingredient
            ) for ingredient in ingredient_set
        ]
        for name, value in recipe_data['recipe'].items():
            self.assertEqual(
                getattr(recipe, name),
                value
            )
        for i, ingredient in enumerate(recipe_data['ingredients']):
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

    def test_serializer_update_recipe(self):
        recipe_data = get_recipe_data('lekker')
        recipe_data['recipe']['instructions'] = "Stir well for 20 minutes"
        recipe, _ = Recipe.recipes.get(pk=self.lekker.pk)
        serializer = RecipeSerializer(
            recipe,
            data=recipe_data
        )
        self.assertTrue(serializer.is_valid())
        recipe = serializer.save()
        ingredient_set = self.lekker.ingredient_set.all()
        ingredient_amounts = [
            IngredientAmount.objects.select_related('amount').get(
                recipe=self.lekker,
                ingredient=ingredient
            ) for ingredient in ingredient_set
        ]
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

    def test_serializer_update_recipe_ingredients(self):
        recipe_data = get_recipe_data('lekker')
        recipe_data['ingredients'][0]['ingredient']['name'] = "zucchino"
        recipe_data['ingredients'][0]['ingredient']['plural'] = "zucchini"
        recipe, _ = Recipe.recipes.get(pk=self.lekker.pk)
        serializer = RecipeSerializer(
            recipe,
            data=recipe_data
        )
        self.assertTrue(serializer.is_valid())
        recipe = serializer.save()
        ingredient_set = self.lekker.ingredient_set.all()
        ingredient_amounts = [
            IngredientAmount.objects.select_related('amount').get(
                recipe=self.lekker,
                ingredient=ingredient
            ) for ingredient in ingredient_set
        ]
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
