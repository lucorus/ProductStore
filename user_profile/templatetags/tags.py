from user_profile.models import Comments
from django import template
register = template.Library()


# возвращает сумму товаров в корзине текущего пользователя
@register.simple_tag(name='sum_basket')
def sum_basket(request=None, queryset=None):
    try:
        user_session = request.session
        ans = 0

        # проходимся по сессии пользователя и умножаем цену каждого товара на его кол-во
        for item in user_session['products']:
            if queryset["product_objects"][item].discount <= 0:
                ans += int(user_session['products'][item]['count']) * int(user_session['products'][item]['price'])
            else:
                ans += int(user_session['products'][item]['count']) * queryset["product_objects"][item].price_with_discount()
        return ans
    except KeyError:
        # если в корзине нет ключа products
        return 0
    except Exception as ex:
        print(f'ex - {ex } ')
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


@register.simple_tag(name='is_favorite')
def is_favorite(request, product_id: int) -> bool:
    try:
        if request.user.favourites.filter(id=product_id).exists():
            return True
        else:
            return False
    except:
        return False
