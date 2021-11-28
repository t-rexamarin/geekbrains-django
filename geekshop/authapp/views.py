from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from authapp.forms import UserLoginForm, UserRegistrationForm, UserChangeProfileForm
from django.shortcuts import render
from baskets.models import Basket


# Create your views here.
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)

            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'GeekShop | Авторизация',
        'form': form
    }

    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)

    return HttpResponseRedirect(reverse('index'))


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)

        if form.is_valid():
            form.save()
            success_txt = 'Registration successful.'
            messages.success(request, success_txt)
            return HttpResponseRedirect(reverse('authapp:login'))
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'GeekShop | Регистрация',
        'form': form
    }

    return render(request, 'authapp/registration.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserChangeProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            success_txt = 'Changes were successfully saved.'
            messages.success(request, success_txt)
            form.save()
        else:
            # messages.set_level(request, messages.ERROR)
            # messages.error(request, form.errors)
            # print(form.errors)
            # print(form.non_field_errors())
            error_txt = 'Changes were successfully saved.'
            messages.error(request, form.errors.as_json())

    context = {
        'title': 'GeekShop | Профиль',
        'form': UserChangeProfileForm(instance=request.user),
        'baskets': Basket.objects.filter(user=request.user)
    }

    return render(request, 'authapp/profile.html', context)
