from django.core.management.base import BaseCommand
from prettytable import PrettyTable
from ordersapp.models import OrderItem
from mainapp.models import Product
from django.db.models import Q, F, When, Case, DecimalField, IntegerField
from datetime import timedelta


class Command(BaseCommand):
    def handle(self, *args, **options):
        ACTION_1 = 1
        ACTION_2 = 2
        ACTION_EXPIRED = 3

        action_1__timedelta = timedelta(hours=12)
        action_2__timedelta = timedelta(days=1)

        action_1__discount = 0.3
        action_2__discount = 0.15
        action_expired__discount = 0.05

        action_1__condition = Q(order__updated_at__lte=F('order__created_at') + action_1__timedelta)
        action_2__condition = Q(order__updated_at__gt=F('order__created_at') +
                                                    action_1__timedelta) & \
                              Q(order__updated_at__lte=F('order__created_at') +
                                                    action_2__timedelta)
        action_expired__condition = Q(order__updated_at__gt=F('order__created_at') +
                                      action_2__timedelta)

        action_1__order = When(action_1__condition, then=ACTION_1)
        action_2__order = When(action_2__condition, then=ACTION_2)
        action_expired__order = When(action_expired__condition, then=ACTION_EXPIRED)

        action_1__price = When(action_1__condition,
                               then=F('product__price') * F('quantity') * action_1__discount)
        action_2__price = When(action_2__condition,
                               then=F('product__price') * F('quantity') * -action_2__discount)
        action_expired__price = When(action_expired__condition,
                                     then=F('product__price') * F('quantity') * action_expired__discount)

        test_orders = OrderItem.objects.annotate(
            action_order=Case(
                action_1__order,
                action_2__order,
                action_expired__order,
                output_field=IntegerField(),
            )).annotate(
            total_price=Case(
                action_1__price,
                action_2__price,
                action_expired__price,
                output_field=DecimalField(),
            )).order_by('action_order', 'total_price').select_related()

        t_list = PrettyTable(['Заказ', 'Товар', 'Скидка', 'Разница времени'])
        t_list.align = 'l'

        for orderitem in test_orders:
            t_list.add_row([f'{orderitem.action_order} заказ №{orderitem.order.pk}', f'{orderitem.product.name:15}',
                            f'{abs(orderitem.total_price):6.2f} руб',
                            orderitem.order.updated_at - orderitem.order.created_at])

        print(t_list)
