from django import template

from products.models import Comments

register = template.Library()


# возвращает сумму товаров в корзине текущего пользователя
@register.simple_tag(name='sum_basket')
def sum_basket(request=None):
    try:
        user_session = request.session
        ans = 0

        for item in user_session['products']:
            ans += int(item['count']) * int(item['price'])
        return ans
    except:
        return 0


# получаем кол-во товаров продукта с названием title
@register.simple_tag(name='get_count')
def get_count(request=None, title=''):
    try:
        user_session = request.session

        # ищем product в сессии с названием title и возвращаем его кол-во
        for item in user_session['products']:
            if item['title'] == title:
                return item['count']

        return 0
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

