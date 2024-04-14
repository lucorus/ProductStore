from django.db import models
from users.models import CustomUser
from products.models import Product


class Basket(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='basket', verbose_name='Владелец корзины')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='basket', verbose_name='Продукт')
    count = models.PositiveSmallIntegerField(default=1, verbose_name='Количество')
    created_add = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def get_count_products_in_basket(self) -> int:
        return Basket.objects.filter(owner=self.owner).count()

    def __str__(self):
        return f'Корзина пользователя {self.owner.username} с товаром {self.product.title}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
