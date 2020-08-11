import os
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from recipes.models import Recipe


class DeleteSingleRecipeTest(APITestCase):
    """ Test deleting an existing recipe """

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
    """ Test deleting an existing recipe without authentication """

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
