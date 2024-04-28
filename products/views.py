from django.db.models import Q, F
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, FormView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from users.forms import UserLoginForm
from . import models, serializers, paginators
from . import utils


def main_page(request):
    return render(request, 'products/main_page.html', {'form': UserLoginForm})


def categories(request):
    return render(request, 'products/categories.html', {'form': UserLoginForm})


class Products(ListAPIView):
    serializer_class = serializers.ProductSerializer
    pagination_class = paginators.CustomPagination

    def get_queryset(self):
        return utils.get_products_by_filter(self.request)


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