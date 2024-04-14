from django.contrib import admin
from django.contrib.admin import register

from . import models


@register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'slug', 'subcategory', 'discount', 'showing']
    prepopulated_fields = {'slug': ('title', )}


@register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'slug', 'image']
    prepopulated_fields = {'slug': ('title',)}


@register(models.SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'slug', 'image']
    prepopulated_fields = {'slug': ('title',)}
