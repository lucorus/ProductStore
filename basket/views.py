from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from rest_framework.views import APIView
from products.models import Product
from users.models import CustomUser
from . import models


class AddBasket(LoginRequiredMixin, APIView):
    def get(self, reqeust, product_slug):
        try:
            product = Product.objects.get(slug=product_slug)
            if product:
                models.Basket.objects.get_or_create(owner=reqeust.user, product=product)
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'error', 'message': 'product does not exists'})
        except Exception as ex:
            print(ex)
            return JsonResponse({'status': 'error'})


class ChangeCountProductInBasket(LoginRequiredMixin, APIView):
    def get(self, request, product_slug, operation):
        try:
            basket = models.Basket.objects.get(owner=request.user, product__slug=product_slug)
            if not basket:
                return JsonResponse({'status': 'error', 'message': 'basket not found'})

            if operation == '-':
                if basket.count < 2:
                    basket.delete()
                else:
                    basket.count -= 1
                    basket.save()
            else:
                basket.count += 1
                basket.save()
            return JsonResponse({'status': 'success'})
        except Exception as ex:
            print(ex)
            return JsonResponse({'status': 'error'})


class DeleteBasket(LoginRequiredMixin, APIView):
    def get(self, request, product_slug):
        try:
            print(product_slug)
            if product_slug == '__all__':
                basket = models.Basket.objects.filter(owner=request.user)
            else:
                basket = models.Basket.objects.get(product__slug=product_slug, owner=request.user)
            basket.delete()
            return JsonResponse({'status': 'success'})
        except Exception as ex:
            print(ex)
            return JsonResponse({'status': 'error'})
