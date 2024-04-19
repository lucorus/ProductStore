from django.db.models import Q
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
        products = models.Product.objects.showing_products().all()
        if self.kwargs.get('slug'):
            products = products.filter(Q(subcategory__category__slug=self.kwargs['slug']) | Q(subcategory__slug=self.kwargs['slug']))
        return products


class CategoriesAPI(ListAPIView):
    serializer_class = serializers.CategoriesSerializer
    pagination_class = paginators.CategoriesPaginator
    queryset = models.Category.objects.all()


class DetailProductInfo(APIView):
    def get(self, request, slug):
        product = models.Product.objects.get(slug=slug)
        serializer = serializers.ProductSerializer(product)
        return JsonResponse({'product': serializer.data})
