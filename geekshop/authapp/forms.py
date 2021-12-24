import hashlib
import random
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from authapp.models import User, UserProfile
from django import forms

from authapp.validators import clean_firstname


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите адрес эл. почты'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save()
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf-8')).hexdigest()
        user.save()
        return user

    # сами определяем валидаторы для полей
    def clean_username(self):
        username = self.cleaned_data['username']
        errors = []
        errors_status = 0

        if User.objects.filter(username=username).exists():
            errors_status = 1
            errors.append(ValidationError(_('Username already taken.')))
            # raise ValidationError(_('Username already taken'))

        banned_usernames = ['банан', 'дурак', 'django']
        username_l = username.lower()
        if username_l in banned_usernames:
            errors_status = 1
            errors.append(ValidationError(_(f'Username {username_l} is not allowed.')))
            # raise ValidationError(_(f'Username {username_l} is not allowed'))

        if errors_status:
            raise ValidationError(errors)

        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError(_('Email already taken.'))
        return email


class UserChangeProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(), validators=[clean_firstname])
    age = forms.IntegerField(widget=forms.NumberInput(), required=False)
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'age', 'image')

    def __init__(self, *args, **kwargs):
        super(UserChangeProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(UserProfileEditForm, self).__init__(*args, **kwargs)
        dropdown_fields = ['gender', 'language']

        for field_name, field in self.fields.items():
            if field_name not in dropdown_fields:
                field.widget.attrs['class'] = 'form-control py-4'
            else:
                field.widget.attrs['class'] = 'form-control'

            if field_name == 'about':
                field.widget.attrs['rows'] = 3
