from django.urls import path
from mainapp.views import products, item

app_name = 'products'
urlpatterns = [
    path('', products, name='products'),
    path('item/<int:id>', item, name='item'),
]
