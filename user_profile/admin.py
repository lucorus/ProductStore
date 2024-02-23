from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'username', 'slug']
    prepopulated_fields = {'slug': ('username',)}


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'product', 'estimation']


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Comments, CommentsAdmin)

