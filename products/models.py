from django.db import models
from django.urls import reverse


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class CustomProductManager(models.Manager):
    def showing_products(self):
        return self.get_queryset().filter(showing=True)


# список фотографий, добавляемых к продукту
class ProductPhoto(models.Model):
    product_photo = models.ImageField(upload_to='products/img/')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Фото продукта'
        verbose_name_plural = 'Фотографии продуктов'


class Product(models.Model):
    title = models.CharField(max_length=256, unique=True, verbose_name='Название')
    slug = models.SlugField()
    price = models.PositiveIntegerField(verbose_name='Цена')
    photos = models.ManyToManyField(ProductPhoto, related_name='product', verbose_name='Фотографии')
    subcategory = models.ForeignKey('SubCategory', on_delete=models.PROTECT, related_name='product', verbose_name='Подкатегория')
    discount = models.DecimalField(default=0, decimal_places=2, max_digits=4, verbose_name='Скидка')
    showing = models.BooleanField(default=True, verbose_name='Отображать?')
    objects = CustomProductManager()

    def price_with_discount(self) -> int:
        ans = round(self.price - (self.price * (self.discount/100)))
        return ans

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Category(models.Model):
    title = models.CharField(max_length=64, unique=True, verbose_name='Название')
    slug = models.SlugField()
    image = models.ImageField(upload_to='products/img/', verbose_name='Изображение')

    def get_absolute_url(self):
        return reverse('products_in_category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class SubCategory(models.Model):
    title = models.CharField(max_length=64, unique=True, verbose_name='Название')
    slug = models.SlugField()
    image = models.ImageField(upload_to='products/img/', verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name='Категория')

    def get_absolute_url(self):
        return reverse('products_in_category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
