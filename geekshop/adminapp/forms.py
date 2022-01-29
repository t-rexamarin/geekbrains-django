from django import forms
from authapp.forms import UserRegistrationForm, UserChangeProfileForm
from authapp.models import User
from mainapp.models import ProductCategory, Product


class UserAdminRegisterForm(UserRegistrationForm):
    is_staff = forms.BooleanField()
    is_active = forms.BooleanField()

    class Meta:
        model = User
        fields = ('username', 'email', 'age', 'image', 'first_name', 'last_name', 'password1', 'password2',
                  'is_staff', 'is_active')

    def __init__(self, *args, **kwargs):
        super(UserAdminRegisterForm, self).__init__(*args, **kwargs)
        required_false = ('is_staff', 'is_active')

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

            if field_name in required_false:
                self.fields[field_name].required = False

        self.fields['image'].widget.attrs['class'] = 'custom-file-input'
        self.fields['first_name'].widget.attrs.update({'autofocus': 'autofocus'})


class UserAdminProfileForm(UserChangeProfileForm):
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
    image = forms.ImageField(widget=forms.FileInput())

    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price', 'quantity', 'is_active')

    def __init__(self, *args, **kwargs):
        super(ProductEditForm, self).__init__(*args, **kwargs)
        dropdown_fields = ['category']

        for field_name, field in self.fields.items():
            if field_name not in dropdown_fields:
                field.widget.attrs['class'] = 'form-control py-4'
            else:
                field.widget.attrs['class'] = 'form-control'

        self.fields['image'].widget.attrs['class'] = 'custom-file-input'


class CategoryUpdateFormAdmin(forms.ModelForm):
    discount = forms.IntegerField(widget=forms.NumberInput(), label='скидка', required=False, min_value=0, max_value=90,
                                  initial=0)

    class Meta:
        model = ProductCategory
        fields = ('name', 'description', 'discount')

    def __init__(self, *args, **kwargs):
        super(CategoryUpdateFormAdmin, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['rows'] = 1
