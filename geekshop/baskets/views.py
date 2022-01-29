from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from baskets.models import Basket
from mainapp.models import Product


@login_required
def basket_add(request, id):
    if request.is_ajax():
        user_select = request.user
        product = Product.objects.get(id=id)
        baskets = Basket.objects.filter(user=user_select, product=product)

        if baskets:
            basket = baskets.first()
            # basket.quantity = F('quantity') + 1
            basket.quantity += 1
            basket.save()
        else:
            Basket.objects.create(user=user_select, product=product, quantity=1)

        products = Product.objects.all()
        context = {'products': products}
        result = render_to_string('mainapp/includes/card.html', context)

        return JsonResponse({'result': result})


class BasketDeleteView(DeleteView):
    model = Basket
    success_url = reverse_lazy('authapp:profile')
    template_name = 'authapp/profile.html'

    def get(self, *args, **kwargs):
        """
        This has been overriden because by default
        DeleteView doesn't work with GET requests
        """
        self.delete(*args, **kwargs)

        if self.request.is_ajax():
            context = super(BasketDeleteView, self).get_context_data(**kwargs)
            baskets = Basket.objects.filter(user=self.request.user)
            context['baskets'] = baskets
            result = render_to_string('baskets/basket.html', context)

            return JsonResponse({'result': result})
        else:
            return HttpResponseRedirect(self.success_url)


@login_required
def basket_edit(request, id_basket, quantity):
    if request.is_ajax():
        basket = Basket.objects.get(id=id_basket)

        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()

        baskets = Basket.objects.filter(user=request.user)
        context = {'baskets': baskets}
        result = render_to_string('baskets/basket.html', context)

        return JsonResponse({'result': result})
