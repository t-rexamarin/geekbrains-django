from django.test import TestCase
from mainapp.models import Product, ProductCategory
from django.test.client import Client


# Create your tests here.
class TestMainSmokeTest(TestCase):
    def setUp(self):
        category = ProductCategory.objects.create(
            name='TestCat1'
        )

        Product.objects.create(
            category=category,
            name='products_test_1',
            price=100
        )

        self.client = Client()

    # def tearDown(self):
    #     pass

    def test_products_pages(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_products_product(self):
        for product_item in Product.objects.all():
            response = self.client.get(f'/products/item/{product_item.pk}')
            self.assertEqual(response.status_code, 200)
