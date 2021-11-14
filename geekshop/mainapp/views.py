from django.shortcuts import render
from .models import Products


# Create your views here.
def index(request):
    context = {
        'title': 'GeekShop from view',
        'header': 'GeekShop Store',
        'header_info': 'Новые образы и лучшие бренды на GeekShop Store. '
                  'Бесплатная доставка по всему миру! Аутлет: до -70% Собственный бренд. -20% новым покупателям.',
        'user': 'User from view'
    }

    return render(request, 'index.html', context)


def products(request):
    return render(request, 'products.html')
