from django.test import TestCase
from django.conf import settings
from django.test.client import Client
from authapp.models import User


# для дебага в параметрах скрипта
# test authapp.tests.UserManagementTestCase.test_login
# Create your tests here.
class UserManagementTestCase(TestCase):
    username = 'django'
    email = 'django@mail.ru'
    password = 'geekshop'

    new_user_data = {
        'username': 'django1',
        'first_name': 'django1',
        'last_name': 'django2',
        'password1': 'zzzxxx111',
        'password2': 'zzzxxx111',
        'email': 'geekshop@rr.rr',
        'age': 30
    }

    def setUp(self):
        self.user = User.objects.create_superuser(self.username, email=self.email, password=self.password)
        self.client = Client()

    def tearDown(self):
        pass

    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/user/login/')
        self.assertEqual(response.status_code, 302)

    def test_registration(self):
        response = self.client.post('/user/registration/', data=self.new_user_data)
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

        new_user = User.objects.get(username=self.new_user_data['username'])
        activation_url = f'{settings.DOMAIN_NAME}/user/verify/{self.new_user_data["email"]}/{new_user.activation_key}'
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 200)

        new_user.refresh_from_db()
        self.assertTrue(new_user.is_active)
