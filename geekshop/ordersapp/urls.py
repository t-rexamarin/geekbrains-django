from django.urls import path
from ordersapp.views import OrderCreate, OrderUpdate, OrderList, OrderDetail, OrderDelete, order_forming_complete, \
    order_status_change, get_product_price

app_name = 'ordersapp'
urlpatterns = [
    path('', OrderList.as_view(), name='list'),
    path('create/', OrderCreate.as_view(), name='create'),
    path('update/<int:pk>/', OrderUpdate.as_view(), name='update'),
    path('read/<int:pk>/', OrderDetail.as_view(), name='read'),
    path('delete/<int:pk>/', OrderDelete.as_view(), name='delete'),
    path('forming_complete/<int:pk>/', order_forming_complete, name='forming_complete'),

    path('change_status/<int:pk>/<int:cancel>', order_status_change, name='change_status'),
    path('get_product_price/<int:pk>/', get_product_price, name='get_product_price'),
]