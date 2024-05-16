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


class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='Товар')
    text = models.TextField(max_length=2048, verbose_name='Текст')
    estimation = models.PositiveSmallIntegerField(blank=True, verbose_name='Оценка')
    answers = models.ManyToManyField('Comment', blank=True, related_name='comment', verbose_name='Ответы')

    def save(self, *args, **kwargs):
        try:
            if int(self.estimation) > 5:
                self.estimation = 5
        finally:
            super().save(*args, **kwargs)

    def count_answers(self) -> int:
        return Comment.objects.filter(answers__pk=self.pk).count()

    def get_answers(self) -> list:
        return list(Comment.objects.select_related('product', 'author').filter(answers__pk=self.pk).values('pk', 'text', 'author__username', 'author__slug'))

    def __str__(self):
        return f'Комментарий от { self.author.username } к товару { self.product.title }'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
