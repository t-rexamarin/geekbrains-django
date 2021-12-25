from django.db import models
from authapp.models import User
from mainapp.models import Product


# Create your models here.
# гда вызываем delete у корзины, возвращаем на склад кол-ва товара
# class BasketQuerySet(models.QuerySet):
#     def delete(self, *args, **kwargs):
#         for item in self:
#             item.product.qunatity += item.quantity
#             item.product.save()
#         super(BasketQuerySet, self).delete(*args, **kwargs)


class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    def total_sum(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.sum() for basket in baskets)

    def total_quantity(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.quantity for basket in baskets)

    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         get_item = self.get_item(int(self.pk))
    #         self.product.quantity -= self.quantity - get_item
    #     else:
    #         self.product.quantity -= self.quantity
    #     self.product.save()
    #     super(Basket, self).save(*args, **kwargs)
    #
    # def delete(self, *args, **kwargs):
    #     self.product.quantity += self.quantity
    #     self.save()
    #     super(Basket, self).delete(*args, **kwargs)

    @staticmethod
    def get_item(pk):
        """
        Возвращает кол-во товаров в корзине
        @param pk: ключ корзины
        @type pk:
        @return:
        @rtype:
        """
        return Basket.objects.get(pk=pk).quantity
