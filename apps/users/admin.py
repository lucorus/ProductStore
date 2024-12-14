from allauth.socialaccount.models import SocialApp
from django.contrib import admin
from django.contrib.admin import register
from . import models


@register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'access_write_comments', 'username', 'slug']
    prepopulated_fields = {'slug': ('username',)}


@register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_filter = ['author', 'product']
    list_display = ['pk', 'showing', 'author', 'product']


@register(models.Complaints)
class ComplaintsAdmin(admin.ModelAdmin):
    list_filter = ['author', 'comment']
    list_display = ['pk', 'is_reviewed', 'author', 'comment']


class SocialAppAdmin(admin.ModelAdmin):
    model = SocialApp
    menu_icon = 'placeholder'
    add_to_settings_menu = False
    exclude_for_explorer = False
    list_display = ['name', 'provider']

