import os
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from recipes.models import Recipe
from recipes.serializers import RecipeListSerializer


class GetAllRecipesTest(APITestCase):
    """ Test getting all recipes """

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
        response = self.client.get(reverse('recipes'))
        recipes = Recipe.objects.all()
        serializer = RecipeListSerializer(recipes, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAllRecipesAsUnauthenticatedTest(APITestCase):
    """ Test getting all recipes without authentication """

    def setUp(self):
        self.lekker = Recipe.objects.create(name='Lekker', servings=3, instructions='Stir well')
        self.pas_mal = Recipe.objects.create(
            name='Pas mal',
            servings=2,
            instructions='Servir sur un lit de choucroute'
        )

    def test_get_all_recipes(self):
        response = self.client.get(reverse('recipes'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
