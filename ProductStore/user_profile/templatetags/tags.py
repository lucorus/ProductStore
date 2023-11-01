from django import template
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
