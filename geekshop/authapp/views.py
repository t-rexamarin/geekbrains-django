from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, UpdateView
from mainapp.mixin import BaseClassContextMixin, UserDispatchMixin
from authapp.forms import UserLoginForm, UserRegistrationForm, UserChangeProfileForm
from django.shortcuts import render, get_object_or_404
from authapp.models import User
from baskets.models import Basket


# Create your views here.
# TODO:
# если логиниться под неактивным аккаунтом, то будет говорить, проверьте пару логин-пароль
# а не то, что аккаунт неактивен. Разобраться с этим моментом
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
            user = form.save()

            if self.send_verify_link(user):
                success_txt = _('Registration successful.')
                messages.success(request, success_txt)
                return HttpResponseRedirect(reverse('authapp:login'))
            else:
                errors = [err_text for err_text in [form_field.errors for form_field in form] if len(err_text) > 0]
                messages.error(request, errors)
        else:
            errors = [err_text for err_text in [form_field.errors for form_field in form] if len(err_text) > 0]
            messages.error(request, errors)

        return render(request, self.template_name, {'form': form})

    def send_verify_link(self, user):
        verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
        subject = _(f'To activate your account {user.username} follow the link')
        message = _(f'To verify your account {user.username} on resource \n{settings.DOMAIN_NAME}{verify_link}')
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def verify(self, email, activation_key):
        try:
            user = User.objects.get(email=email)
            if user and user.activation_key == activation_key and not user.is_activation_key_expires():
                user.activation_key = ''
                user.activation_key_expires = None
                user.is_active = True
                user.save()
                auth.login(self, user)

            return render(self, 'authapp/verification.html')
        except Exception as e:
            print(e)
            return HttpResponseRedirect(reverse('index'))


class ProfileFormView(UpdateView, BaseClassContextMixin, UserDispatchMixin):
    form_class = UserChangeProfileForm
    template_name = 'authapp/profile.html'
    title = 'GeekShop | Профиль'
    success_url = 'authapp:profile'

    def form_valid(self, form):
        success_txt = _('Changes were successfully saved.')
        messages.success(self.request, success_txt)
        super().form_valid(form)

        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, *args, **kwargs):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(ProfileFormView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.request.user)

        return context
