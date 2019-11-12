import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Recipe
from ..serializers import RecipeSerializer


client = Client()  # pylint: disable=invalid-name

class GetAllRecipesTest(TestCase):
    """ Test module for GET all recipes API """

    def setUp(self):
        self.lekker = Recipe.objects.create(name='Lekker', servings=3, instructions='Stir well')
        self.pas_mal = Recipe.objects.create(
            name='Pas mal',
            servings=2,
            instructions='Servir sur un lit de choucroute'
        )

    def tearDown(self):
        Recipe.objects.all().delete()

    def test_get_all_recipes(self):
        # get API response
        response = client.get(reverse('recipe_list'))
        # get data from db
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetSingleRecipeTest(TestCase):
    """ Test module for GET single recipe API """

    def setUp(self):
        self.lekker = Recipe.objects.create(name='Lekker', servings=3, instructions='Stir well')
        self.pas_mal = Recipe.objects.create(
            name='Pas mal',
            servings=2,
            instructions='Servir sur un lit de choucroute'
        )

    def tearDown(self):
        Recipe.objects.all().delete()

    def test_get_valid_single_recipe(self):
        response = client.get(
            reverse('recipe_detail', kwargs={'pk': self.lekker.pk}))
        recipe = Recipe.objects.get(pk=self.lekker.pk)
        serializer = RecipeSerializer(recipe)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_recipe(self):
        response = client.get(
            reverse('recipe_detail', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CreateNewRecipeTest(TestCase):
    """ Test module for inserting a new recipe """

    def setUp(self):
        self.valid_payload = dict(name='Lekker', servings=3, instructions='Stir well')
        self.invalid_payload = dict(
            name='',
            servings=2,
            instructions='Servir sur un lit de choucroute'
        )

    def tearDown(self):
        Recipe.objects.all().delete()

    def test_create_valid_recipe(self):
        response = client.post(
            reverse('recipe_list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(
            {key: response.data[key] for key in self.valid_payload.keys()},
            self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_recipe(self):
        response = client.post(
            reverse('recipe_list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateSingleRecipeTest(TestCase):
    """ Test module for updating an existing recipe """

    def setUp(self):
        self.lekker = Recipe.objects.create(name='Lekker', servings=3, instructions='Stir well')
        self.pas_mal = Recipe.objects.create(
            name='Pas mal',
            servings=2,
            instructions='Servir sur un lit de choucroute'
        )
        self.valid_payload = dict(name='Lekker', servings=3, instructions='Stir for 2 hours')
        self.invalid_payload = dict(
            name='',
            servings=2,
            instructions='Servir sur un lit de choucroute et fenouil'
        )

    def tearDown(self):
        Recipe.objects.all().delete()

    def test_valid_update_recipe(self):
        response = client.put(
            reverse('recipe_detail', kwargs={'pk': self.lekker.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        recipe = Recipe.objects.get(pk=self.lekker.pk)
        serializer = RecipeSerializer(recipe)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_recipe(self):
        response = client.put(
            reverse('recipe_detail', kwargs={'pk': self.pas_mal.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteSingleRecipeTest(TestCase):
    """ Test module for deleting an existing recipe """

    def setUp(self):
        self.lekker = Recipe.objects.create(name='Lekker', servings=3, instructions='Stir well')
        self.pas_mal = Recipe.objects.create(
            name='Pas mal',
            servings=2,
            instructions='Servir sur un lit de choucroute'
        )

    def tearDown(self):
        Recipe.objects.all().delete()

    def test_valid_delete_recipe(self):
        response = client.delete(
            reverse('recipe_detail', kwargs={'pk': self.lekker.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_recipe(self):
        response = client.delete(
            reverse('recipe_detail', kwargs={'pk': self.pas_mal.pk + 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
