import json
import os
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Recipe
from ..serializers import RecipeSerializer, RecipeListSerializer


class GetAllRecipesTest(APITestCase):

    def setUp(self):
        self.user = User.objects.get(username=os.environ['AUTH0_USERNAME'])
        self.client.force_authenticate(user=self.user) # pylint: disable=no-member
        self.lekker = Recipe.objects.create(name='Lekker', servings=3, instructions='Stir well')
        self.pas_mal = Recipe.objects.create(
            name='Pas mal',
            servings=2,
            instructions='Servir sur un lit de choucroute'
        )

    def tearDown(self):
        self.client.force_authenticate(user=None) # pylint: disable=no-member

    def test_get_all_recipes(self):
        response = self.client.get(reverse('recipe_list'))
        recipes = Recipe.objects.all()
        serializer = RecipeListSerializer(recipes, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAllRecipesAsUnauthenticatedTest(APITestCase):
    """ Test module for GET all recipes API without authentication """

    def setUp(self):
        self.lekker = Recipe.objects.create(name='Lekker', servings=3, instructions='Stir well')
        self.pas_mal = Recipe.objects.create(
            name='Pas mal',
            servings=2,
            instructions='Servir sur un lit de choucroute'
        )

    def test_get_all_recipes(self):
        response = self.client.get(reverse('recipe_list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetSingleRecipeTest(APITestCase):
    """ Test module for GET single recipe API """

    def setUp(self):
        self.user = User.objects.get(username=os.environ['AUTH0_USERNAME'])
        self.client.force_authenticate(user=self.user) # pylint: disable=no-member
        self.lekker = Recipe.objects.create(name='Lekker', servings=3, instructions='Stir well')
        self.pas_mal = Recipe.objects.create(
            name='Pas mal',
            servings=2,
            instructions='Servir sur un lit de choucroute'
        )

    def tearDown(self):
        self.client.force_authenticate(user=None) # pylint: disable=no-member

    def test_get_valid_single_recipe(self):
        response = self.client.get(
            reverse('recipe_detail', kwargs={'pk': self.lekker.pk}))
        recipe = Recipe.objects.get(pk=self.lekker.pk)
        serializer = RecipeSerializer(recipe)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_recipe(self):
        response = self.client.get(
            reverse('recipe_detail', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetSingleRecipeUnauthenticatedTest(APITestCase):
    """ Test module for GET single recipe API without authentication """

    def setUp(self):
        self.lekker = Recipe.objects.create(name='Lekker', servings=3, instructions='Stir well')
        self.pas_mal = Recipe.objects.create(
            name='Pas mal',
            servings=2,
            instructions='Servir sur un lit de choucroute'
        )

    def test_get_valid_single_recipe(self):
        response = self.client.get(
            reverse('recipe_detail', kwargs={'pk': self.lekker.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_invalid_single_recipe(self):
        response = self.client.get(
            reverse('recipe_detail', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateNewRecipeTest(APITestCase):
    """ Test module for inserting a new recipe """

    def setUp(self):
        self.user = User.objects.get(username=os.environ['AUTH0_USERNAME'])
        self.client.force_authenticate(user=self.user) # pylint: disable=no-member
        self.valid_payload = dict(name='Lekker', servings=3, instructions='Stir well')
        self.invalid_payload = dict(
            name='',
            servings=2,
            instructions='Servir sur un lit de choucroute'
        )

    def tearDown(self):
        self.client.force_authenticate(user=None) # pylint: disable=no-member

    def test_create_valid_recipe(self):
        response = self.client.post(
            reverse('recipe_list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(
            {key: response.data[key] for key in self.valid_payload},
            self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_recipe(self):
        response = self.client.post(
            reverse('recipe_list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreateNewRecipeUnauthenticatedTest(APITestCase):
    """ Test module for inserting a new recipe without authentication """

    def setUp(self):
        self.valid_payload = dict(name='Lekker', servings=3, instructions='Stir well')
        self.invalid_payload = dict(
            name='',
            servings=2,
            instructions='Servir sur un lit de choucroute'
        )

    def test_create_valid_recipe(self):
        response = self.client.post(
            reverse('recipe_list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_invalid_recipe(self):
        response = self.client.post(
            reverse('recipe_list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateSingleRecipeTest(APITestCase):
    """ Test module for updating an existing recipe """

    def setUp(self):
        self.user = User.objects.get(username=os.environ['AUTH0_USERNAME'])
        self.client.force_authenticate(user=self.user) # pylint: disable=no-member
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
        self.client.force_authenticate(user=None) # pylint: disable=no-member

    def test_valid_update_recipe(self):
        response = self.client.put(
            reverse('recipe_detail', kwargs={'pk': self.lekker.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        recipe = Recipe.objects.get(pk=self.lekker.pk)
        serializer = RecipeSerializer(recipe)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_recipe(self):
        response = self.client.put(
            reverse('recipe_detail', kwargs={'pk': self.pas_mal.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleRecipeUnauthenticatedTest(APITestCase):
    """ Test module for updating an existing recipe without authentication """

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

    def test_valid_update_recipe(self):
        response = self.client.put(
            reverse('recipe_detail', kwargs={'pk': self.lekker.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_update_recipe(self):
        response = self.client.put(
            reverse('recipe_detail', kwargs={'pk': self.pas_mal.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DeleteSingleRecipeTest(APITestCase):
    """ Test module for deleting an existing recipe """

    def setUp(self):
        self.user = User.objects.get(username=os.environ['AUTH0_USERNAME'])
        self.client.force_authenticate(user=self.user) # pylint: disable=no-member
        self.lekker = Recipe.objects.create(name='Lekker', servings=3, instructions='Stir well')
        self.pas_mal = Recipe.objects.create(
            name='Pas mal',
            servings=2,
            instructions='Servir sur un lit de choucroute'
        )

    def tearDown(self):
        self.client.force_authenticate(user=None) # pylint: disable=no-member

    def test_valid_delete_recipe(self):
        response = self.client.delete(
            reverse('recipe_detail', kwargs={'pk': self.lekker.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_recipe(self):
        response = self.client.delete(
            reverse('recipe_detail', kwargs={'pk': self.pas_mal.pk + 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteSingleRecipeUnauthenticatedTest(APITestCase):
    """ Test module for deleting an existing recipe without authentication """

    def setUp(self):
        self.lekker = Recipe.objects.create(name='Lekker', servings=3, instructions='Stir well')
        self.pas_mal = Recipe.objects.create(
            name='Pas mal',
            servings=2,
            instructions='Servir sur un lit de choucroute'
        )

    def test_valid_delete_recipe(self):
        response = self.client.delete(
            reverse('recipe_detail', kwargs={'pk': self.lekker.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_delete_recipe(self):
        response = self.client.delete(
            reverse('recipe_detail', kwargs={'pk': self.pas_mal.pk + 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
