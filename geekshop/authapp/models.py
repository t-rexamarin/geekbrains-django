from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    ENGLISH = 'ENGLISH'
    RUSSIAN = 'RUSSIAN'

    LANGUAGE_CHOICES = (
        (ENGLISH, 'English'),
        (RUSSIAN, 'Русский'),
    )

    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    about = models.TextField(verbose_name='о себе', blank=True, null=True)
    gender = models.CharField(verbose_name='пол', choices=GENDER_CHOICES, blank=True, max_length=2)
    language = models.CharField(verbose_name='язык', blank=True, choices=LANGUAGE_CHOICES, default=ENGLISH, max_length=20)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()
