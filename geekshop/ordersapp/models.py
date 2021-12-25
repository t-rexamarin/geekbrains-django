from django.conf import settings
from django.db import models
from django.utils.timezone import now

from baskets.models import Basket
from mainapp.models import Product
from django.utils.translation import gettext as _


# Create your models here.
class Order(models.Model):
    FORMING = 'FM'
    SEND_TO_PROCEED = 'STP'
    PAID = 'PD'
    PROCEEDED = 'PRD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, _('формируется')),
        (SEND_TO_PROCEED, _('отправлен в обработку')),
        (PAID, _('оплачено')),
        (PROCEEDED, _('обрабатывается')),
        (READY, _('готов к выдаче')),
        (CANCEL, _('отмена заказа')),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, verbose_name='статус', max_length=3, default=FORMING)
    is_active = models.BooleanField(verbose_name='активный', default=True)
    created_at = models.DateTimeField(verbose_name='дата создания', default=now)
    updated_at = models.DateTimeField(verbose_name='дата изменения', auto_now=True)

    def __str__(self):
        return _(f'Текущий заказ {self.pk}')

    # TODO:
    # разобраться с select_related()
    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.get_product_cost(), items)))

    def get_items(self):
        pass

    def delete(self, using=None, keep_parents=False):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.save()
        self.is_active = False
        self.save()

    # TODO:
    # поэксперементировать с выводом в темплейт
    def get_current_status(self):
        return self.status


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='заказ', related_name='orderitems', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='продукты', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk).quantity
