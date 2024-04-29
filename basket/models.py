from django.db import models
from users.models import CustomUser
from products.models import Product


class Basket(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='basket', verbose_name='Владелец корзины')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='basket', verbose_name='Продукт')
    count = models.PositiveSmallIntegerField(default=1, verbose_name='Количество')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    # возвращает кол-во предметов в корзине пользователя
    def get_count_products_in_basket(self) -> int:
        return Basket.objects.filter(owner=self.owner).count()

    # возвращает сумму предметов в корзине пользователя
    def get_sum_products(self) -> int:
        try:
            basket = Basket.objects.filter(owner=self.owner)
            total = 0
            for item in basket:
                total += item.product.price_with_discount() * item.count
            return total
        except Exception as ex:
            print(ex)
            return 0

    def __str__(self):
        return f'Корзина пользователя {self.owner.username} с товаром {self.product.title}'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
