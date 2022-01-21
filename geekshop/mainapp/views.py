from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page, never_cache

from .models import Product, ProductCategory
from django.conf import settings
from django.core.cache import cache


# Create your views here.
def get_link_category():
    if settings.LOW_CACHE:
        key = 'link_category'
        link_category = cache.get(key)
        if link_category is None:
            link_category = ProductCategory.objects.all()
            cache.set(key, link_category)

        return link_category
    else:
        return ProductCategory.objects.all()


def get_link_product():
    if settings.LOW_CACHE:
        key = 'link_product'
        link_product = cache.get(key)
        if link_product is None:
            link_product = Product.objects.all().select_related('category')
            cache.set(key, link_product)

        return link_product
    else:
        return Product.objects.all().select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product{pk}'
        product = cache.get(key)
        if product is None:
            product = Product.objects.get(pk=pk)
            cache.set(key, product)

        return product
    else:
        return Product.objects.get(pk=pk)


def index(request):
    context = {
        'title': 'GeekShop',
        'header': 'GeekShop Store',
        'header_info': 'Новые образы и лучшие бренды на GeekShop Store. '
                  'Бесплатная доставка по всему миру! Аутлет: до -70% Собственный бренд. -20% новым покупателям.',
    }

    return render(request, 'mainapp/index.html', context)


# TODO:
# получается запутанная ситуация при фильтрации категорий и навигационной панелью пагинации
# т.к. если отфильтровать по категории, а потом нажать на страницу пагинации в панели
# то вернет на страницу пагинации всех товаров, без учета категории
# как то определять, что мы находимся на отфильтрованной категории?
# @cache_page(3600)
# @never_cache
def products(request, category_id=None, page=1):
    if category_id:
        # products = Product.objects.filter(category_id=category_id)
        # select_related вытащит все связанные модели
        products = Product.objects.filter(category_id=category_id).select_related('category')
    else:
        # products = Product.objects.all()
        products = Product.objects.all().select_related('category')

    products = get_link_product()

    # products_categories = ProductCategory.objects.all()
    products_categories = get_link_category()
    paginator = Paginator(products, per_page=3)

    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': 'GeekShop | Каталог',
        'productsCategories': products_categories,
        'products': products_paginator
    }

    if request.is_ajax():
        result = render_to_string('mainapp/includes/card.html', context)
        return JsonResponse({'result': result})
    else:
        return render(request, 'mainapp/products.html', context)


def item(request, id):
    # product = Product.objects.get(id=id).select_related()
    context = {
        'title': 'GeekShop | Детали товара',
        # 'product': product
        'product': get_product(id)
    }

    return render(request, 'mainapp/item.html', context)
