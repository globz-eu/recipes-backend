import json
from .. import reverse, status, Authenticate, SetPayloads


class CreateNewRecipeTest(Authenticate, SetPayloads):
    """ Test creating a new recipe """

    def setUp(self):
        Authenticate.setUp(self)
        SetPayloads.setUp(self)

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


class CreateNewRecipeUnauthenticatedTest(SetPayloads):
    """ Test creating a new recipe without authentication """

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
