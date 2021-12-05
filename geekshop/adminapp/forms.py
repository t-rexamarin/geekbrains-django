from django import forms
from authapp.forms import UserRegistrationForm, UserChangeProfileForm
from authapp.models import User
from mainapp.models import ProductCategory, Product


class UserAdminRegisterForm(UserRegistrationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'age', 'image', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserAdminRegisterForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

        self.fields['image'].widget.attrs['class'] = 'custom-file-input'


class UserAdminProfileForm(UserChangeProfileForm):
    # email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control py-4', 'readonly': False}))
    # username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control py-4', 'readonly': False}))
    email = forms.EmailField(widget=forms.EmailInput())
    username = forms.CharField(widget=forms.TextInput())

    def __init__(self, *args, **kwargs):
        super(UserAdminProfileForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['readonly'] = False
        self.fields['username'].widget.attrs['readonly'] = False
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

        self.fields['image'].widget.attrs['class'] = 'custom-file-input'


class ProductCategoryEditForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('name', 'description', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['rows'] = 1
        # self.fields['description'].widget.attrs['columns'] = 15


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price', 'quantity', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['rows'] = 1
        # self.fields['description'].widget.attrs['columns'] = 15