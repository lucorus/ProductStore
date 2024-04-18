from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, FormView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from users.forms import UserLoginForm
from . import models, serializers


def main_page(request):
    return render(request, 'products/main_page.html', {'form': UserLoginForm})


class CustomPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100


class Products(ListAPIView):
    serializer_class = serializers.ProductSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        products = models.Product.objects.showing_products().all()
        if self.kwargs.get('category_slug'):
            products = products.filter(subcategory__category__slug=self.kwargs['category_slug'])
        if self.kwargs.get('subcategory_slug'):
            products = products.filter(subcategory__slug=self.kwargs['subcategory_slug'])
        return products


class CategoriesView(ListView, FormView):
    template_name = 'products/categories.html'
    context_object_name = 'product'
    form_class = UserLoginForm
    paginate_by = 2
    queryset = products = models.Category.objects.all().order_by('-id')


class DetailProductInfo(APIView):
    def get(self, request, slug):
        product = models.Product.objects.get(slug=slug)
        serializer = serializers.ProductSerializer(product)
        return JsonResponse({'product': serializer.data})
