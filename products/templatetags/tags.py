from django import template
from products.models import Product
from basket.models import Basket
register = template.Library()


# возвращает сумму товаров в корзине текущего пользователя
@register.simple_tag(name='sum_basket')
def sum_basket(request=None, queryset=None):
    try:
        ans = 0

        # проходимся по сессии пользователя и умножаем цену каждого товара на его кол-во
        basket = Basket.objects.filter(owner=request.user).values('product__price', 'count')
        print(f'basket = {basket}')
        for item in basket:
            ans += item.product.price * item.count
        return ans
    except KeyError:
        # если в корзине нет ключа products
        return 0
    except Exception as ex:
        print(f'ex - {ex } ')
        return 0


# получаем кол-во товаров продукта с названием title
@register.simple_tag(name='get_count')
def get_count(request=None, slug='') -> int:
    try:
        product = Product.objects.get(slug=slug)
        return Basket.objects.get(product=product, owner=request.user).count
    except Exception as ex:
        print(ex)
        return 0
