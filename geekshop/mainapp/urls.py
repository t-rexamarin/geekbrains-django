from django.urls import path
from mainapp.views import products, item

app_name = 'products'
urlpatterns = [
    path('', products, name='products'),
    path('page/<int:page>', products, name='page'),
    path('item/<int:id>', item, name='item'),
    path('category/<int:category_id>/<int:page>', products, name='category'),
]
