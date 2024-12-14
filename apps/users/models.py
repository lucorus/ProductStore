from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.models import BaseSlugField
from apps.products.models import Product


class CustomUser(AbstractUser, BaseSlugField):
    username = models.CharField(max_length=40, unique=True, blank=True, verbose_name='Имя пользователя')
    favorites = models.ManyToManyField(Product, related_name='users', blank=True, verbose_name='Избранное')
    slug = models.SlugField()
    access_write_comments = models.BooleanField(default=True, verbose_name='Пользователь может писать комментарии?')

    def count_created_complaints(self) -> int:
        return Complaints.objects.filter(author=self).count()

    def count_received_complaints(self) -> int:
        return Comment.objects.filter(author=self).exclude(complaints=None).count()

    def count_comments(self) -> int:
        return Comment.objects.filter(author=self).count()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class CustomCommentManager(models.Manager):
    def showing_comments(self):
        return self.get_queryset().filter(showing=True)


class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='Товар')
    text = models.TextField(max_length=2048, verbose_name='Текст')
    estimation = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Оценка')
    answers = models.ManyToManyField('Comment', blank=True, related_name='comment', verbose_name='Ответы')
    showing = models.BooleanField(default=True, verbose_name='Отображать')
    objects = CustomCommentManager()

    def count_answers(self) -> int:
        return Comment.objects.filter(comment__pk=self.pk).count()

    def get_answers(self) -> list:
        return list(Comment.objects.select_related('product', 'author').filter(comment__pk=self.pk).values('pk', 'text', 'author__username', 'author__slug'))

    def __str__(self):
        return f'Комментарий от { self.author.username } к товару { self.product.title }'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Complaints(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_complaints', verbose_name='Автор')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='complaints', verbose_name='Комментарий')
    is_reviewed = models.BooleanField(default=False, verbose_name='Рассмотрено?')

    # при сохранении жалобы, если is_reviewed=True, то все жалобы на тот же комментарий, что и текущая будут рассмотрены
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, change_other_complaints=True):
        if self.is_reviewed and change_other_complaints:
            complaints = Complaints.objects.filter(comment=self.comment)
            complaints.update(is_reviewed=True)
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'Жалоба от {self.author} на комментарий {self.comment}'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'
