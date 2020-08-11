import json
import os
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer


class UpdateSingleRecipeTest(APITestCase):
    """ Test updating an existing recipe """

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
    """ Test updating an existing recipe without authentication """

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
