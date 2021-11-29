from django.shortcuts import render
from .models import Product, ProductCategory


# Create your views here.
def index(request):
    context = {
        'title': 'GeekShop',
        'header': 'GeekShop Store',
        'header_info': 'Новые образы и лучшие бренды на GeekShop Store. '
                  'Бесплатная доставка по всему миру! Аутлет: до -70% Собственный бренд. -20% новым покупателям.',
    }

    return render(request, 'mainapp/index.html', context)


def products(request):
    productsCategories = ProductCategory.objects.all()
    products = Product.objects.all()
    context = {
        'title': 'GeekShop | Каталог',
        'productsCategories': productsCategories,
        'products': products
    }

    return render(request, 'mainapp/products.html', context)


def item(request, id):
    product = Product.objects.get(id=id)
    context = {
        'title': 'GeekShop | Детали товара',
        'product': product
    }

    return render(request, 'mainapp/item.html', context)

