from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from adminapp.forms import UserAdminRegisterForm, UserAdminProfileForm, ProductCategoryEditForm, ProductEditForm
from authapp.models import User
from mainapp.mixin import BaseClassContentMixin, CustomDispatchMixin
from mainapp.models import ProductCategory, Product


# Create your views here.
# TODO:
# удаление и работа с деактивацией в одном классе вместо 3? через проверку прав?
# допустим если вы супер админ добавьте флаг на форму который подтвердит удаления
# если валидно - удалить, если нет, деактивировать


class IndexTemplateView(TemplateView, BaseClassContentMixin, CustomDispatchMixin):
    template_name = 'adminapp/admin.html'
    title = 'GeekShop | Admin'


class UserListView(ListView, BaseClassContentMixin, CustomDispatchMixin):
    model = User
    template_name = 'adminapp/admin-users-read.html'
    title = 'Админка | Пользователи'


class UserCreateView(CreateView, BaseClassContentMixin, CustomDispatchMixin):
    model = User
    template_name = 'adminapp/admin-users-create.html'
    title = 'Админка | Пользователи'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('adminapp:admin_users')


class UserUpdateView(UpdateView, BaseClassContentMixin, CustomDispatchMixin):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    title = 'Админка | Редактирование пользователя'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('adminapp:admin_users')


class UserDeleteView(DeleteView, CustomDispatchMixin):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('adminapp:admin_users')


class UserDeactivateDeleteView(DeleteView, CustomDispatchMixin):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('adminapp:admin_users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.is_active:
            self.object.is_active = False
            self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class UserRestoreDeleteView(DeleteView, CustomDispatchMixin):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('adminapp:admin_users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.is_active is False:
            self.object.is_active = True
            self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class CategoryListView(ListView, BaseClassContentMixin, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'adminapp/admin-categories-read.html'
    title = 'Админка | Категории'


class CategoryCreateView(CreateView, BaseClassContentMixin, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'adminapp/admin-categories-create.html'
    title = 'Админка | Создать категорию'
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('adminapp:admin_categories')


class CategoryUpdateView(UpdateView, BaseClassContentMixin, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'adminapp/admin-categories-update-delete.html'
    title = 'Админка | Редактировать категорию'
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('adminapp:admin_categories')


class CategoryDeleteView(DeleteView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'adminapp/admin-categories-update-delete.html'
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('adminapp:admin_categories')


class CategoryDeactivateDeleteView(DeleteView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'adminapp/admin-categories-update-delete.html'
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('adminapp:admin_categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.is_active:
            self.object.is_active = False
            self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class CategoryRestoreDeleteView(DeleteView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'adminapp/admin-categories-update-delete.html'
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('adminapp:admin_categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.is_active is False:
            self.object.is_active = True
            self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductListView(ListView, BaseClassContentMixin, CustomDispatchMixin):
    model = Product
    template_name = 'adminapp/admin-products-read.html'
    title = 'Админка | Продукты'


class ProductCreateView(CreateView, BaseClassContentMixin, CustomDispatchMixin):
    model = Product
    template_name = 'adminapp/admin-products-create.html'
    title = 'Админка | Создание продукта'
    form_class = ProductEditForm
    success_url = reverse_lazy('adminapp:admin_products')


class ProductUpdateView(UpdateView, BaseClassContentMixin, CustomDispatchMixin):
    model = Product
    template_name = 'adminapp/admin-products-update-delete.html'
    title = 'Админка | Редактирование продукта'
    form_class = ProductEditForm
    success_url = reverse_lazy('adminapp:admin_products')


class ProductDeleteView(DeleteView, CustomDispatchMixin):
    model = Product
    template_name = 'adminapp/admin-products-update-delete.html'
    form_class = ProductEditForm
    success_url = reverse_lazy('adminapp:admin_products')


class ProductDeactivateDeleteView(DeleteView, CustomDispatchMixin):
    model = Product
    template_name = 'adminapp/admin-products-update-delete.html'
    form_class = ProductEditForm
    success_url = reverse_lazy('adminapp:admin_products')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.is_active:
            self.object.is_active = False
            self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductRestoreDeleteView(DeleteView, CustomDispatchMixin):
    model = Product
    template_name = 'adminapp/admin-products-update-delete.html'
    form_class = ProductEditForm
    success_url = reverse_lazy('adminapp:admin_products')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.is_active is False:
            self.object.is_active = True
            self.object.save()

        return HttpResponseRedirect(self.get_success_url())
