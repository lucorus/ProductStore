from django.contrib import admin
from django.contrib.admin import register
from . import models


@register(models.CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'username', 'slug']
    prepopulated_fields = {'slug': ('username',)}
