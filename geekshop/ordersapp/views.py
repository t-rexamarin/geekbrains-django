from django.db import transaction
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView


# Create your views here.
from baskets.models import Basket
from mainapp.mixin import BaseClassContextMixin
from mainapp.models import Product
from ordersapp.forms import OrderItemsForm
from ordersapp.models import Order, OrderItem


class OrderList(ListView, BaseClassContextMixin):
    model = Order
    title = _('Geekshop | Список заказов')

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)


class OrderCreate(CreateView, BaseClassContextMixin):
    model = Order
    fields = []
    title = _('Geekshop | Создание заказа')
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_item = Basket.objects.filter(user=self.request.user).select_related('product')

            if basket_item:
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=basket_item.count())
                formset = OrderFormSet()

                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_item[num].product
                    form.initial['quantity'] = basket_item[num].quantity
                    form.initial['price'] = basket_item[num].product.price

                # basket_item.delete()
            else:
                formset = OrderFormSet()

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()

            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            if self.object.get_total_cost() == 0:
                self.object.delete()
        
        return super(OrderCreate, self).form_valid(form)
                

class OrderUpdate(UpdateView):
    model = Order
    fields = []
    title = _('Geekshop | Обновление заказа')
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            if self.object.get_total_cost() == 0:
                self.object.delete()

        return super(OrderUpdate, self).form_valid(form)


class OrderDelete(DeleteView, BaseClassContextMixin):
    model = Order
    title = _('Geekshop | Удаление заказа')
    success_url = reverse_lazy('orders:list')


class OrderDetail(DetailView, BaseClassContextMixin):
    model = Order
    title = _('Geekshop | Просмотр заказа')


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SEND_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('orders:list'))


# TODO:
# подумать, как не хардкодить статусы в темплейте
def order_status_change(request, pk, cancel=0):
    order = get_object_or_404(Order, pk=pk)

    if cancel:
        order.status = Order.CANCEL
    else:
        if order.status == Order.FORMING:
            order.status = Order.SEND_TO_PROCEED
        elif order.status == Order.SEND_TO_PROCEED:
            order.status = Order.PAID
        elif order.status == Order.PAID:
            order.status = Order.PROCEEDED
        elif order.status == Order.PROCEEDED:
            order.status = Order.READY

    order.save()
    return HttpResponseRedirect(reverse('orders:list'))


def get_product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.get(pk=pk)

        if product:
            price = product.price
            return JsonResponse({'price': price})
        else:
            return JsonResponse({'price': 0})


# # вызывается при сохранении корзины или заказа
@receiver(pre_save, sender=Basket)
@receiver(pre_save, sender=OrderItem)
def product_quantity_update_save(sender, instance, **kwargs):
    if instance.pk:
        get_item = instance.get_item(int(instance.pk))
        instance.product.quantity -= instance.quantity - get_item
    else:
        instance.product.quantity -= instance.quantity

    instance.product.save()


# вызывается при удалении корзины или заказа
@receiver(pre_delete, sender=Basket)
@receiver(pre_delete, sender=OrderItem)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()
