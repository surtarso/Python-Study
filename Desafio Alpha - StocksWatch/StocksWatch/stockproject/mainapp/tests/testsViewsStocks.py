from django.test import TestCase
from mainapp.models import Mercado


class TestStockpickerViews(TestCase):
    
        @classmethod
        def setUpTestData(cls):
            cls.IBOV = Mercado.objects.create(name='IBOV')
            cls.IFIX = Mercado.objects.create(name='IFIX')
    
        def setUp(self):
            self.mercados = Mercado.objects.all()
            
        def test_markets_exist(self):
            self.assertTrue(len(self.mercados) > 0)
    
        # def test_stockpicker_view_exists(self):
        #     response = self.client.get('/stockpicker/')
        #     self.assertEqual(response.status_code, 200)
    
        # def test_stockpicker_view_uses_correct_template(self):
        #     response = self.client.get('/stockpicker/')
        #     self.assertTemplateUsed(response, 'stockpicker/stockpicker.html')
    
        



