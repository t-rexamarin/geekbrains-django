from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
from authapp.models import User
import json


def load_from_json(file_name):
    with open(file_name, mode='r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        CATEGORIES_PATH = 'mainapp/fixtures/categories.json'
        PRODUCTS_PATH = 'mainapp/fixtures/products.json'

        categories = load_from_json(CATEGORIES_PATH)
        ProductCategory.objects.all().delete()
        for category in categories:
            cat = category.get('fields')
            cat['id'] = category.get('pk')
            new_category = ProductCategory(**cat)
            new_category.save()

        products = load_from_json(PRODUCTS_PATH)
        Product.objects.all().delete()
        for product in products:
            prod = product.get('fields')
            category = prod.get('category')
            _category = ProductCategory.objects.get(id=category)
            prod['category'] = _category
            new_product = Product(**prod)
            new_product.save()

        super_user = User.objects.create_superuser('django', '', '1')
