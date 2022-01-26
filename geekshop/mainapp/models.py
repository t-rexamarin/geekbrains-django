from django.db import models


# Create your models here.
class ActiveCategoryManager(models.Manager):
    def get_queryset(self):
        return super(ActiveCategoryManager, self).get_queryset().filter(is_active=True)


class ProductCategory(models.Model):
    objects = models.Manager()
    active_categories = ActiveCategoryManager()

    name = models.CharField(verbose_name='имя', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', max_length=128, blank=True)
    created_at = models.DateTimeField(verbose_name='дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='дата изменения', auto_now=True)
    is_active = models.BooleanField(verbose_name='активна', default=True, db_index=True)

    # def __str__(self):
    #     return self.name

    class Meta:
        verbose_name_plural = "ProductCategory"


class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super(ActiveProductManager, self).get_queryset().filter(is_active=True)


class Product(models.Model):
    objects = models.Manager()
    active_products = ActiveProductManager()

    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='имя продукта', max_length=128)
    image = models.ImageField(upload_to='product_image', blank=True)
    description = models.CharField(verbose_name='краткое описание продукта', max_length=128, blank=True)
    price = models.DecimalField(verbose_name='цена продукта', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='количество на складе', default=0)
    created_at = models.DateTimeField(verbose_name='дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='дата изменения', auto_now=True)
    is_active = models.BooleanField(verbose_name='активна', default=True, db_index=True)

    def __str__(self):
        # убирает 3 десятка буликатов в редактировании заказа
        # return f"{self.name} ({self.category.name})"
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Product"
