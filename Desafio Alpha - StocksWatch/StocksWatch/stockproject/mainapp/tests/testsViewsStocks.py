from django.http import QueryDict
from django.test import TestCase
from mainapp.models import Mercado

class TestStockpickerMarkets(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.IBOV = Mercado.objects.create(name='IBOV')
        cls.IFIX = Mercado.objects.create(name='IFIX')

    def setUp(self):
        self.mercados = Mercado.objects.all()
        
    def test_markets_exist(self):
        self.assertTrue(len(self.mercados) > 0)
