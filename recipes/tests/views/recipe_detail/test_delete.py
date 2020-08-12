from .. import status, reverse, InitializeRecipes, Authenticate


class DeleteSingleRecipeTest(InitializeRecipes, Authenticate):
    """ Test deleting an existing recipe """

    def setUp(self):
        InitializeRecipes.setUp(self)
        Authenticate.setUp(self)

    def test_valid_delete_recipe(self):
        response = self.client.delete(
            reverse('recipe_detail', kwargs={'pk': self.lekker.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_recipe(self):
        response = self.client.delete(
            reverse('recipe_detail', kwargs={'pk': self.pas_mal.pk + 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteSingleRecipeUnauthenticatedTest(InitializeRecipes):
    """ Test deleting an existing recipe without authentication """

    def test_valid_delete_recipe(self):
        response = self.client.delete(
            reverse('recipe_detail', kwargs={'pk': self.lekker.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_delete_recipe(self):
        response = self.client.delete(
            reverse('recipe_detail', kwargs={'pk': self.pas_mal.pk + 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
