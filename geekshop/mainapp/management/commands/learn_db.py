from django.core.management.base import BaseCommand
from django.db import connection
from adminapp.views import db_profile_by_type
from mainapp.models import Product
from django.db.models import Q, F


class Command(BaseCommand):
    def handle(self, *args, **options):
        products = Product.objects.filter(
            # ~Q(category__name='Одежда')
            # Q(category__name='Обувь') | Q(category__name='Одежда')
            Q(category__name='Обувь') & Q(category__id=4)
        )

        print(products)
        db_profile_by_type('learn db', '', connection.queries)
