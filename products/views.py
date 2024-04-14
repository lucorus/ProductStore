from django.shortcuts import render
from django.views.generic import ListView, FormView
from users.forms import UserLoginForm
from . import models


class MainPage(ListView, FormView):
    template_name = 'products/main_page.html'
    context_object_name = 'product'
    form_class = UserLoginForm
    paginate_by = 3

    def get_queryset(self):
        products = models.Product.objects.showing_products().select_related('subcategory').all().defer(
            'subcategory__category__slug',
            'subcategory__category__image',
            'subcategory__image',
            'subcategory__slug',
            'showing').order_by('id')
        return products


class CategoriesView(ListView, FormView):
    template_name = 'products/categories.html'
    context_object_name = 'product'
    form_class = UserLoginForm
    paginate_by = 2
    queryset = products = models.Category.objects.all().order_by('-id')

