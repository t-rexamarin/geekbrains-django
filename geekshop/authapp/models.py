from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


# Create your models here.
class User(AbstractUser):
    image = models.ImageField(upload_to='users_image', blank=True)
    age = models.PositiveIntegerField(default=18)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(auto_now=True, blank=True, null=True)
    # created_at = models.DateTimeField(verbose_name='дата создания', auto_now_add=True)
    # если указывать now(), а не now, то при создании миграции будет высвечивать ворнинг Fixed default value provided
    created_at = models.DateTimeField(verbose_name='дата создания', default=now)
    updated_at = models.DateTimeField(verbose_name='дата изменения', auto_now=True)

    def is_activation_key_expires(self):
        if now() <= self.activation_key_expires + timedelta(hours=48):
            return False
        else:
            return True
