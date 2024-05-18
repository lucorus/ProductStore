from allauth.socialaccount.models import SocialApp
from django.contrib import admin
from django.contrib.admin import register
from . import models


@register(models.CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'username', 'slug']
    prepopulated_fields = {'slug': ('username',)}


@register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'author', 'product']


class SocialAppAdmin(admin.ModelAdmin):
    model = SocialApp
    menu_icon = 'placeholder'
    add_to_settings_menu = False
    exclude_for_explorer = False
    list_display = ['name', 'provider']

