from django.contrib import auth, messages
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
