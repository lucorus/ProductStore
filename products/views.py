from django.db.models import Q, F
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, FormView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from users.forms import UserLoginForm
from . import models, serializers, paginators


def main_page(request):
    return render(request, 'products/main_page.html', {'form': UserLoginForm})


def categories(request):
    return render(request, 'products/categories.html', {'form': UserLoginForm})


class Products(ListAPIView):
    serializer_class = serializers.ProductSerializer
    pagination_class = paginators.CustomPagination

    def get_queryset(self):
        min_price = self.request.GET.get('min_price') or 0
        max_price = self.request.GET.get('max_price') or 99999999999
        sorting = self.request.GET.get('sorting') or '-id'
        category = self.request.GET.get('category') or 'Null'
        subcategory = self.request.GET.get('subcategory') or 'Null'

        products = models.Product.objects.showing_products().\
            annotate(discount_price=F('price') - (F('price') * F('discount')/100))\
            .filter(Q(discount_price__gte=min_price) & Q(discount_price__lte=max_price)).order_by(sorting)
        if category != 'Null':
            products = products.filter(subcategory__category__slug=category)
        if subcategory != 'Null':
            products = products.filter(subcategory__slug=subcategory)
        return products


class CategoriesAPI(ListAPIView):
    serializer_class = serializers.CategoriesSerializer
    pagination_class = paginators.CategoriesPaginator
    queryset = models.Category.objects.all()


class DetailProductInfo(APIView):
    def get(self, request, slug):
        try:
            product = models.Product.objects.get(slug=slug)
            serializer = serializers.ProductSerializer(product)
            return JsonResponse({'status': 'success', 'product': serializer.data})
        except Exception as ex:
            print(ex)
            return JsonResponse({'status': 'error', 'message': 'product not exists'})