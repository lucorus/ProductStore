from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from products.models import Product, IntegerRangeField


class CustomUser(AbstractUser):
    username = models.CharField(max_length=40, unique=True, blank=True, verbose_name='Имя пользователя')
    favourites = models.ManyToManyField(Product, related_name='users', blank=True, verbose_name='Избранное')
    slug = models.SlugField()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(CustomUser, self).save(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        if self.estimation > 5:
            self.estimation = 5
        if self.estimation < 1:
            self.estimation = 1
        super(Comments, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'



