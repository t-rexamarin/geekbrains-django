from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
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


def products(request, page=1):
    productsCategories = ProductCategory.objects.all()
    products = Product.objects.all()
    paginator = Paginator(products, per_page=3)

    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': 'GeekShop | Каталог',
        'productsCategories': productsCategories,
        'products': products_paginator
    }

    return render(request, 'mainapp/products.html', context)


def item(request, id):
    product = Product.objects.get(id=id)
    context = {
        'title': 'GeekShop | Детали товара',
        'product': product
    }

    return render(request, 'mainapp/item.html', context)


# def category(request, id):
#     productsCategories = ProductCategory.objects.all()
#     products = Product.objects.filter(category=id)
#     context = {
#         'title': 'GeekShop | Категория',
#         'productsCategories': productsCategories,
#         'products': products
#     }
#
#     # for cat in productsCategories:
#         # print(translit(cat, 'ru', reversed=True))
#         # print(type(cat.name))
#
#     return render(request, 'mainapp/products.html', context)

# TODO:
# перенести в products
def category(request, id):
    if request.is_ajax():
        productsCategories = ProductCategory.objects.all()
        products = Product.objects.filter(category=id)
        context = {
            'title': 'GeekShop | Категория',
            'productsCategories': productsCategories,
            'products': products
        }

        result = render_to_string('mainapp/includes/card.html', context)

        return JsonResponse({'result': result})
