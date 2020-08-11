import json
import os
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User


class CreateNewRecipeTest(APITestCase):
    """ Test creating a new recipe """

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
            reverse('recipes'),
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
            reverse('recipes'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreateNewRecipeUnauthenticatedTest(APITestCase):
    """ Test creating a new recipe without authentication """

    def setUp(self):
        self.valid_payload = dict(name='Lekker', servings=3, instructions='Stir well')
        self.invalid_payload = dict(
            name='',
            servings=2,
            instructions='Servir sur un lit de choucroute'
        )

    def test_create_valid_recipe(self):
        response = self.client.post(
            reverse('recipes'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_invalid_recipe(self):
        response = self.client.post(
            reverse('recipes'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
