from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from adminapp.forms import UserAdminRegisterForm, UserAdminProfileForm, ProductCategoryEditForm, ProductEditForm
from authapp.models import User


# Create your views here.
from mainapp.models import ProductCategory, Product


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'adminapp/admin.html')


@user_passes_test(lambda u: u.is_superuser)
def admin_users(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'adminapp/admin-users-read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_create(request):
    if request.method == 'POST':
        form = UserAdminRegisterForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:admin_users'))
    else:
        form = UserAdminRegisterForm()

    context = {
        'title': 'Geekshop - Админ | Регистрация',
        'form': form
    }

    return render(request, 'adminapp/admin-users-create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_update(request, pk):
    user_select = User.objects.get(pk=pk)

    if request.method == 'POST':
        form = UserAdminProfileForm(data=request.POST, instance=user_select, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:admin_users'))
    else:
        form = UserAdminProfileForm(instance=user_select)

    context = {
        'title': 'Geekshop - Админ | Редактирование пользователя',
        'form': form,
        'user_select': user_select
    }

    return render(request, 'adminapp/admin-users-update-delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_delete(request, pk):
    if request.method == 'POST':
        user = User.objects.get(pk=pk)
        user.is_active = False
        user.save()

    return HttpResponseRedirect(reverse('adminapp:admin_users'))


@user_passes_test(lambda u: u.is_superuser)
def admin_categories(request):
    context = {
        'categories': ProductCategory.objects.all()
    }
    return render(request, 'adminapp/admin-categories-read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_categories_create(request):
    if request.method == 'POST':
        form = ProductCategoryEditForm(data=request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:admin_categories'))
    else:
        form = ProductCategoryEditForm()

    context = {
        'title': 'Geekshop - Админ | Категории товара',
        'form': form
    }

    return render(request, 'adminapp/admin-categories-create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_categories_update(request, pk):
    category_select = ProductCategory.objects.get(pk=pk)

    if request.method == 'POST':
        form = ProductCategoryEditForm(data=request.POST, instance=category_select)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:admin_categories'))
    else:
        form = ProductCategoryEditForm(instance=category_select)

    context = {
        'title': 'Geekshop - Админ | Редактирование категории',
        'form': form,
        'category_select': category_select
    }

    return render(request, 'adminapp/admin-categories-update-delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_categories_delete(request, pk):
    if request.method == 'POST':
        user = ProductCategory.objects.get(pk=pk)
        user.is_active = False
        user.save()

    return HttpResponseRedirect(reverse('adminapp:admin_categories'))


@user_passes_test(lambda u: u.is_superuser)
def admin_products(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'adminapp/admin-products-read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_products_create(request):
    if request.method == 'POST':
        form = ProductEditForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:admin_products'))
    else:
        form = ProductEditForm()

    context = {
        'title': 'Geekshop - Админ | Товары',
        'form': form
    }

    return render(request, 'adminapp/admin-products-create.html', context)