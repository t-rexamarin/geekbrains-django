from django.db import models


# Create your models here.
class Products(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128)
    description = models.TextField(verbose_name='Описание', blank=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name, self.description, self.price
