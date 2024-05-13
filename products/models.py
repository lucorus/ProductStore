from django.urls import reverse
from django.db import models
# from django.utils.text import slugify
from slugify import slugify


class CustomProductManager(models.Manager):
    def showing_products(self):
        return self.get_queryset().filter(showing=True)


class Product(models.Model):
    title = models.CharField(max_length=256, unique=True, verbose_name='Название')
    slug = models.SlugField()
    price = models.PositiveIntegerField(verbose_name='Цена')
    photo = models.ImageField(upload_to='products/img/products/', blank=True, verbose_name='Фотографии')
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE, related_name='product', verbose_name='Подкатегория')
    discount = models.DecimalField(default=0, decimal_places=2, max_digits=4, verbose_name='Скидка')
    showing = models.BooleanField(default=True, verbose_name='Отображать?')
    objects = CustomProductManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def price_with_discount(self) -> int:
        return round(self.price - (self.price * (self.discount/100)))

    def get_absolute_url(self):
        return reverse('products:product_detail_view', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Category(models.Model):
    title = models.CharField(max_length=64, unique=True, verbose_name='Название')
    slug = models.SlugField()
    image = models.ImageField(upload_to='products/img/category/', blank=True, verbose_name='Изображение')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('products:category_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class SubCategory(models.Model):
    title = models.CharField(max_length=64, unique=True, verbose_name='Название')
    slug = models.SlugField()
    image = models.ImageField(upload_to='products/img/subcategory/', blank=True, verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name='Категория')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('products:category_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
