from django.shortcuts import render


# Create your views here.
from authapp.models import User


def index(request):
    return render(request, 'adminapp/admin.html')


def admin_users(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'adminapp/admin-users-read.html')


def admin_users_create(request):
    return render(request, 'adminapp/admin-users-create.html')


def admin_users_update(request):
    return render(request, 'adminapp/admin-users-update-delete.html')


def admin_users_delete(request):
    return render(request, 'adminapp/admin-users-update-delete.html')
