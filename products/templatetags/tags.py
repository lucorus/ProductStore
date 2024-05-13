from django import template
from products.models import Product, Category, SubCategory
from basket.models import Basket
register = template.Library()


# возвращает сумму товаров в корзине текущего пользователя
@register.simple_tag(name='get_categories')
def get_categories():
    return Category.objects.all().order_by('title').values('title', 'slug')


@register.simple_tag(name='get_subcategories')
def get_subcategories():
    return SubCategory.objects.all().order_by('title').values('title', 'slug')


# получаем кол-во товаров с переданным slug'ом в корзине request.user
@register.simple_tag(name='get_count')
def get_count(request, slug: str) -> int:
    try:
        if request.user.is_authenticated:
            product = Product.objects.get(slug=slug)
            basket = Basket.objects.get(owner=request.user, product=product)
            return basket.count
        else:
            return 0
    except Exception as ex:
        return 0
