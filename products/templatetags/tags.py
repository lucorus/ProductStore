from django import template
from products.models import Product, Category, SubCategory
from basket.models import Basket
register = template.Library()


# возвращает сумму товаров в корзине текущего пользователя
@register.simple_tag(name='get_categories')
def get_categories():
    return Category.objects.all().order_by('title')


@register.simple_tag(name='get_subcategories')
def get_subcategories():
    return SubCategory.objects.all().order_by('title')
