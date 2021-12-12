from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, UpdateView
from mainapp.mixin import BaseClassContextMixin, UserDispatchMixin
from authapp.forms import UserLoginForm, UserRegistrationForm, UserChangeProfileForm
from django.shortcuts import render, get_object_or_404
from authapp.models import User
from baskets.models import Basket


# Create your views here.
class LoginListView(LoginView, BaseClassContextMixin):
    template_name = 'authapp/login.html'
    form_class = UserLoginForm
    title = 'GeekShop | Авторизация'


class Logout(LogoutView):
    template_name = 'mainapp/index.html'


class RegistrationListView(FormView, BaseClassContextMixin):
    model = User
    form_class = UserRegistrationForm
    template_name = 'authapp/registration.html'
    title = 'GeekShop | Регистрация'
    success_url = reverse_lazy('authapp:login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            form.save()
            success_txt = 'Registration successful.'
            messages.success(request, success_txt)
            return HttpResponseRedirect(reverse('authapp:login'))
        else:
            errors = [err_text for err_text in [form_field.errors for form_field in form] if len(err_text) > 0]
            messages.error(request, errors)

        return render(request, self.template_name, {'form': form})


class ProfileFormView(UpdateView, BaseClassContextMixin, UserDispatchMixin):
    form_class = UserChangeProfileForm
    template_name = 'authapp/profile.html'
    title = 'GeekShop | Профиль'
    success_url = 'authapp:profile'

    def form_valid(self, form):
        success_txt = 'Changes were successfully saved.'
        messages.success(self.request, success_txt)
        super(ProfileFormView, self).form_valid()

        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, *args, **kwargs):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(ProfileFormView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.request.user)

        return context
