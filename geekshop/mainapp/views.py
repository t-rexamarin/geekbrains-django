from django.shortcuts import render
from .models import Product, ProductCategory


# Create your views here.
def index(request):
    context = {
        'title': 'GeekShop',
        'header': 'GeekShop Store',
        'header_info': 'Новые образы и лучшие бренды на GeekShop Store. '
                  'Бесплатная доставка по всему миру! Аутлет: до -70% Собственный бренд. -20% новым покупателям.',
        'user': 'User from view'
    }

    return render(request, 'mainapp/index.html', context)


def products(request):
    products = Product.objects.all()
    context = {
        'title': 'GeekShop - Каталог',
        'products': products
    }

    return render(request, 'mainapp/products.html', context)
