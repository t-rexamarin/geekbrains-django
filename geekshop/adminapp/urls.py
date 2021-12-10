from django.urls import path
from adminapp.views import index, UserListView, UserCreateView, UserUpdateView, UserDeleteView, \
    admin_categories_create, admin_categories_update, admin_categories_delete, admin_products, \
    admin_products_create, admin_products_update, admin_products_delete, admin_categories_restore, \
    admin_products_restore, UserDeactivateDeleteView, UserRestoreDeleteView, CategoriesListView

app_name = 'adminapp'
urlpatterns = [
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admin_users'),
    path('users-create/', UserCreateView.as_view(), name='admin_users_create'),
    path('users-update/<int:pk>', UserUpdateView.as_view(), name='admin_users_update'),
    path('users-delete/<int:pk>', UserDeleteView.as_view(), name='admin_users_delete'),
    path('users-deactivate/<int:pk>', UserDeactivateDeleteView.as_view(), name='admin_users_deactivate'),
    path('users-restore/<int:pk>', UserRestoreDeleteView.as_view(), name='admin_users_restore'),

    path('categories/', CategoriesListView.as_view(), name='admin_categories'),
    path('categories-create/', admin_categories_create, name='admin_categories_create'),
    path('categories-update/<int:pk>', admin_categories_update, name='admin_categories_update'),
    path('categories-delete/<int:pk>', admin_categories_delete, name='admin_categories_delete'),
    path('categories-restore/<int:pk>', admin_categories_restore, name='admin_categories_restore'),

    path('products/', admin_products, name='admin_products'),
    path('products-create/', admin_products_create, name='admin_products_create'),
    path('products-update/<int:pk>', admin_products_update, name='admin_products_update'),
    path('products-delete/<int:pk>', admin_products_delete, name='admin_products_delete'),
    path('products-restore/<int:pk>', admin_products_restore, name='admin_products_restore'),
]
