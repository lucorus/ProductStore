from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from rest_framework.views import APIView
from products.models import Product
from . import models


class AddBasket(LoginRequiredMixin, APIView):
    def post(self, reqeust, product_slug):
        try:
            product = Product.objects.get(slug=product_slug)
            if product:
                basket = models.Basket.objects.create(owner=reqeust.user, product=product)
                basket.save()
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'error', 'message': 'product does not exists'})
        except:
            return JsonResponse({'status': 'error'})

