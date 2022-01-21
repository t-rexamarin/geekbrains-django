from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, UpdateView
from mainapp.mixin import BaseClassContextMixin, UserDispatchMixin
from authapp.forms import UserLoginForm, UserRegistrationForm, UserChangeProfileForm, UserProfileEditForm
from django.shortcuts import render, get_object_or_404, redirect
from authapp.models import User, UserProfile


# Create your views here.
# TODO:
# 1) если логиниться под неактивным аккаунтом, то будет говорить, проверьте пару логин-пароль
# а не то, что аккаунт неактивен. Разобраться с этим моментом
# 2) resend email наверно стоит как то через verify делать

class LoginListView(LoginView, BaseClassContextMixin):
    template_name = 'authapp/login.html'
    form_class = UserLoginForm
    title = 'GeekShop | Авторизация'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        # return HttpResponseRedirect(reverse('authapp:login'))
        else:
            context = {
                'form': self.form_class
            }

            return render(request, self.template_name, context)


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
                messages.success(request, success_txt, extra_tags='registration_success')
                # messages.add_message(request, messages.SUCCESS, success_txt, extra_tags='registration_success')
                return self.email_confirmation(user)
                # return HttpResponseRedirect(reverse('authapp:email-confirmation'))
                # return HttpResponseRedirect(reverse('authapp:login'))
                # return render(self.request, 'authapp/verification.html', args=[user.email, user.activation_key])
                # return HttpResponseRedirect(reverse('authapp:resend', args=[user.email, user.activation_key]))
            else:
                errors = [err_text for err_text in [form_field.errors for form_field in form] if len(err_text) > 0]
                messages.error(request, errors)
        else:
            errors = [err_text for err_text in [form_field.errors for form_field in form] if len(err_text) > 0]
            messages.error(request, errors)

        return render(request, self.template_name, {'form': form})

    def send_verify_link(self, user):
        verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
        # subject = _(f'To activate your account {user.username} follow the link')
        subject = _(f'Account {user.username} activation')
        message = _(f'To verify your account {user.username} on resource {settings.DOMAIN_NAME}\n'
                    f'click the link {settings.DOMAIN_NAME}{verify_link}')
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def verify(self, email, activation_key):
        try:
            user = User.objects.get(email=email)
            if user and user.activation_key == activation_key and not user.is_activation_key_expires():
                user.activation_key = ''
                user.activation_key_expires = None
                user.is_active = True
                user.save()
                auth.login(self, user, backend=settings.AUTHENTICATION_BACKENDS[0])

            return render(self, 'authapp/verification.html')
        except Exception as e:
            return HttpResponseRedirect(reverse('index'))

    # тут что то страшное
    # пришлось вытягивать из головы крупицы знаний по ООП
    # все это пришлось сделать из-за того, что в self приходил реквест, а не класс
    @classmethod
    def get_user(cls, request, email):
        user = User.objects.get(email=email)
        context = {
            'email': user.email
        }

        if user:
            if cls.send_verify_link(cls, user):
                return render(request, 'authapp/verification.html', context=context)

    def email_confirmation(self, user):
        email = user.email
        activation_key = user.activation_key

        context = {
            # это анонимный юзер, под которым мы находимся в данный момент
            # чтобы user.is_authenticated вел себя корректно в шаблоне
            'user': self.request.user,
            'email': email,
            'activation_key': activation_key
        }
        return render(self.request, 'authapp/verification.html', context=context)
        # return HttpResponseRedirect(reverse('authapp:resend', args=[self.user.email, self.user.activation_key]))


class ProfileFormView(UpdateView, BaseClassContextMixin, UserDispatchMixin):
    form_class = UserChangeProfileForm
    template_name = 'authapp/profile.html'
    title = 'GeekShop | Профиль'
    success_url = 'authapp:profile'

    def post(self, request, *args, **kwargs):
        form = UserProfileEditForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, instance=request.user.userprofile)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            return redirect(self.success_url)

    def form_valid(self, form):
        success_txt = _('Changes were successfully saved.')
        messages.success(self.request, success_txt)
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, *args, **kwargs):
        return get_object_or_404(User, pk=self.request.user.pk)
        # return UserProfile.objects.filter(user=self.request.user.pk).select_related().first()

    def get_context_data(self, **kwargs):
        context = super(ProfileFormView, self).get_context_data(**kwargs)
        context['profile'] = UserProfileEditForm(instance=self.request.user.userprofile)
        return context
