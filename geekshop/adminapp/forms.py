from django import forms
from authapp.forms import UserRegistrationForm
from authapp.models import User


class UserAdminRegisterForm(UserRegistrationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'age', 'image', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserAdminRegisterForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'
