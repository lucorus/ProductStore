from products.models import Comments
from django import template
register = template.Library()


# возвращает сумму товаров в корзине текущего пользователя
@register.simple_tag(name='sum_basket')
def sum_basket(request=None):
    try:
        user_session = request.session
        ans = 0

        # проходимся по сессии пользователя и умножаем цену каждого товара на его кол-во
        for item in user_session['products']:
            ans += int(user_session['products'][item]['count']) * int(user_session['products'][item]['price'])
        return ans
    except:
        return 0


# получаем кол-во товаров продукта с названием title
@register.simple_tag(name='get_count')
def get_count(request=None, title=''):
    try:
        user_session = request.session
        return user_session['products'][title]['count']
    except:
        return 0


@register.simple_tag(name='get_comments')
def get_comments(product_name=''):
    try:
        return Comments.objects.filter(product__title=product_name)
    except:
        return {}


@register.simple_tag(name='length')
def length(text):
    return len(str(text))
