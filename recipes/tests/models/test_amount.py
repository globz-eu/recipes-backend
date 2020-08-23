from django.test import TestCase
from recipes.models import Amount, Unit


class AmountTest(TestCase):

    def setUp(self):
        unit = Unit.objects.create(name='mililiter')
        self.amount = Amount.objects.create(unit=unit, quantity=20)

    def test_db_fields(self):
        amount = Amount.objects.get(pk=self.amount.pk)
        self.assertEqual(amount.quantity, 20)
        self.assertEqual(amount.unit.name, 'mililiter')
