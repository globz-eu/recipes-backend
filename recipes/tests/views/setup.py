import os
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from recipes.models import Recipe


class InitializeRecipes(APITestCase):
    """ Initialize 2 recipes """

    def setUp(self):
        self.lekker = Recipe.objects.create(name='Lekker', servings=3, instructions='Stir well')
        self.pas_mal = Recipe.objects.create(
            name='Pas mal',
            servings=2,
            instructions='Servir sur un lit de choucroute'
        )


class Authenticate(APITestCase):
    def setUp(self):
        self.user = User.objects.get(username=os.environ['AUTH0_USERNAME'])
        self.client.force_authenticate(user=self.user) # pylint: disable=no-member

    def tearDown(self):
        self.client.force_authenticate(user=None) # pylint: disable=no-member


class SetPayloads(APITestCase):
    def setUp(self):
        self.valid_payload = dict(name='Lekker', servings=3, instructions='Stir well')
        self.invalid_payload = dict(
            name='',
            servings=2,
            instructions='Servir sur un lit de choucroute'
        )
