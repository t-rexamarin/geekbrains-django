from django.urls import path
from adminapp.views import IndexTemplateView, UserListView, UserCreateView, UserUpdateView, UserDeleteView, \
    UserDeactivateDeleteView, UserRestoreDeleteView, CategoryListView, CategoryCreateView, \
    CategoryUpdateView, CategoryDeleteView, CategoryDeactivateDeleteView, CategoryRestoreDeleteView, ProductListView, \
    ProductCreateView, ProductUpdateView, ProductDeleteView, ProductRestoreDeleteView, ProductDeactivateDeleteView

app_name = 'adminapp'
urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('users/', UserListView.as_view(), name='admin_users'),
    path('users-create/', UserCreateView.as_view(), name='admin_users_create'),
    path('users-update/<int:pk>', UserUpdateView.as_view(), name='admin_users_update'),
    path('users-delete/<int:pk>', UserDeleteView.as_view(), name='admin_users_delete'),
    path('users-deactivate/<int:pk>', UserDeactivateDeleteView.as_view(), name='admin_users_deactivate'),
    path('users-restore/<int:pk>', UserRestoreDeleteView.as_view(), name='admin_users_restore'),

    path('categories/', CategoryListView.as_view(), name='admin_categories'),
    path('categories-create/', CategoryCreateView.as_view(), name='admin_categories_create'),
    path('categories-update/<int:pk>', CategoryUpdateView.as_view(), name='admin_categories_update'),
    path('categories-delete/<int:pk>', CategoryDeleteView.as_view(), name='admin_categories_delete'),
    path('categories-deactivate/<int:pk>', CategoryDeactivateDeleteView.as_view(), name='admin_categories_deactivate'),
    path('categories-restore/<int:pk>', CategoryRestoreDeleteView.as_view(), name='admin_categories_restore'),

    path('products/', ProductListView.as_view(), name='admin_products'),
    path('products-create/', ProductCreateView.as_view(), name='admin_products_create'),
    path('products-update/<int:pk>', ProductUpdateView.as_view(), name='admin_products_update'),
    path('products-delete/<int:pk>', ProductDeleteView.as_view(), name='admin_products_delete'),
    path('products-deactivate/<int:pk>', ProductDeactivateDeleteView.as_view(), name='admin_products_deactivate'),
    path('products-restore/<int:pk>', ProductRestoreDeleteView.as_view(), name='admin_products_restore'),
]
