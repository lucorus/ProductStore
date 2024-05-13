from django.contrib.auth.models import AbstractUser
from django.db import models
from slugify import slugify
from products.models import Product


class CustomUser(AbstractUser):
    username = models.CharField(max_length=40, unique=True, blank=True, verbose_name='Имя пользователя')
    favorites = models.ManyToManyField(Product, related_name='users', blank=True, verbose_name='Избранное')
    slug = models.SlugField()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
