from django.urls import path
from mainapp.views import products, item, category

app_name = 'products'
urlpatterns = [
    path('', products, name='products'),
    path('page/<int:page>', products, name='page'),
    path('item/<int:id>', item, name='item'),
    path('<int:id>', category, name='category'),
]
