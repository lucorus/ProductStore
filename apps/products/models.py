from django.db.models import Q
from django.db import models

from apps.core.models import BaseSlugField


class CustomProductManager(models.Manager):
    def showing_products(self):
        return self.get_queryset().filter(showing=True)


class Product(BaseSlugField):
    title = models.CharField(max_length=256, unique=True, verbose_name='Название')
    price = models.PositiveIntegerField(verbose_name='Цена')
    photo = models.ImageField(upload_to='products/img/products/', blank=True, verbose_name='Фотографии')
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE, related_name='product', verbose_name='Подкатегория')
    discount = models.DecimalField(default=0, decimal_places=2, max_digits=4, verbose_name='Скидка')
    showing = models.BooleanField(default=True, verbose_name='Отображать?')
    objects = CustomProductManager()

    # получаем среднее арифметическое всех оценок продукта
    def get_estimation(self) -> float:
        try:
            estimations = list(self.comments.filter(Q(product__pk=self.pk) & Q(answers=None)).values('estimation'))
            estimations = [int(item['estimation']) for item in estimations]
            return round(sum(estimations) / len(estimations), 2)
        except:
            return 0

    def price_with_discount(self) -> int:
        return round(self.price - (self.price * (self.discount/100)))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Category(BaseSlugField):
    title = models.CharField(max_length=64, unique=True, verbose_name='Название')
    image = models.ImageField(upload_to='products/img/category/', blank=True, verbose_name='Изображение')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class SubCategory(BaseSlugField):
    title = models.CharField(max_length=64, unique=True, verbose_name='Название')
    image = models.ImageField(upload_to='products/img/subcategory/', blank=True, verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name='Категория')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
