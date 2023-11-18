from django.contrib import admin
from .models import *


class ProductPhotoAdmin(admin.ModelAdmin):
    list_display = ['pk', 'product_photo']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'slug', 'subcategory']
    prepopulated_fields = {'slug': ('title', )}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'slug', 'image']
    prepopulated_fields = {'slug': ('title',)}


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'slug', 'image']
    prepopulated_fields = {'slug': ('title',)}


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'author', 'product']


admin.site.register(Comments, CommentsAdmin)
admin.site.register(ProductPhoto, ProductPhotoAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
