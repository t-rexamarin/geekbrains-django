from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from authapp.forms import UserLoginForm, UserRegistrationForm
from django.shortcuts import render


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
            # при дебаге он не принтует ошибке мне в консоль. Мб дело в коммунити
            print(form.errors)
    else:
        form = UserLoginForm()

    context = {
        'title': 'GeekShop | Авторизация',
        'form': form
    }

    return render(request, 'authapp/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('authapp:login'))
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'GeekShop | Регистрация',
        'form': form
    }

    return render(request, 'authapp/registration.html', context)