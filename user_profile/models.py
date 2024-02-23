from django.contrib.auth.models import AbstractUser
from django.db import models
from products.models import Product


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=40, unique=True, blank=True, verbose_name='Имя пользователя')
    favourites = models.ManyToManyField(Product, related_name='users', blank=True, verbose_name='Избранное')
    slug = models.SlugField()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Comments(models.Model):
    text = models.TextField(max_length=6500, verbose_name='Текст')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='Продукт')
    estimation = IntegerRangeField(min_value=0, max_value=5, default=5, verbose_name='Оценка')

    def __str__(self):
        return f'Комментарий № { self.pk }'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'



