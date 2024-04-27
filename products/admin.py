from django.contrib import admin
from django.contrib.admin import register
from . import models, forms


@register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'slug', 'subcategory', 'discount', 'showing']
    list_display_links = ['pk', 'title', 'slug']
    form = forms.ProductForm
    list_per_page = 50


@register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'image', 'slug']
    list_display_links = ['pk', 'title']
    form = forms.CategoryForm
    list_per_page = 50


@register(models.SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'slug', 'image']
    list_display_links = ['pk', 'title', 'slug']
    form = forms.SubCategoryForm
    list_per_page = 50
