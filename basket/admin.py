from django.contrib import admin
from django.contrib.admin import register
from . import models


@register(models.Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'product', 'count', 'created_add']

