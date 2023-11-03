from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from user_profile.forms import UserLoginForm
from . import models


class MainView(View):
    def get(self, request):
        products = models.Product.objects.select_related('subcategory').all().defer('subcategory__category__slug',
                                                                                    'subcategory__category__image',
                                                                                    'subcategory__image',
                                                                                    'subcategory__slug')
        return render(request, 'products/main_page.html', {'product': products, 'form': UserLoginForm()})


# детальная информация о продукте
class ProductDetailView(View):
    def get(self, request, slug):
        product = models.Product.objects.select_related('subcategory').get(slug=slug)
        return render(request, 'products/detail.html', {'product': product, 'form': UserLoginForm()})


# выводим все категории и подкатегории
class CategoryView(View):
    def get(self, request):
        category = Paginator(models.Category.objects.all().order_by('-id'), 1)
        page_number = request.GET.get('page')
        page_object = category.get_page(page_number)
        return render(request, 'products/categories.html', {'categories': page_object, 'form': UserLoginForm()})


