from django.contrib.postgres.search import SearchVector
from django.db.models import F, Q
from . import models
import logging

logger = logging.getLogger('main')


def get_products_by_filter(request):
    try:
        word = request.GET.get('word') or None
        min_price = request.GET.get('min_price') or 0
        max_price = request.GET.get('max_price') or 99999999999
        sorting = request.GET.get('sorting') or '-id'
        category = request.GET.get('category') or 'Null'
        subcategory = request.GET.get('subcategory') or 'Null'

        products = models.Product.objects.showing_products().select_related('subcategory'). \
            annotate(discount_price=F('price') - (F('price') * F('discount') / 100)) \
            .filter(Q(discount_price__gte=min_price) & Q(discount_price__lte=max_price)).order_by(sorting)
        if category != 'Null':
            products = products.filter(subcategory__category__slug=category)
        if subcategory != 'Null':
            products = products.filter(subcategory__slug=subcategory)
        if word:
            products = models.Product.objects.annotate(
                search=SearchVector('title', 'subcategory__title', 'subcategory__category__title')).filter(search=word)
            vector = SearchVector('title', weight='A') + SearchVector('subcategory__title', weight='B') \
                     + SearchVector('subcategory__category__title', weight='C')
            models.Product.objects.annotate(rank=SearchVector(vector, products)).order_by('rank')
        return products
    except Exception as ex:
        logger.error(ex)
        return []
