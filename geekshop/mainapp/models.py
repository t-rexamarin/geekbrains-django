from django.db import models


# Create your models here.
class Products(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128)
    description = models.TextField(verbose_name='Описание', blank=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=8, decimal_places=2)
    img_name = models.TextField(verbose_name='Название картинки', blank=True)

    objects = models.Manager()
