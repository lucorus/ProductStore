from django.contrib.postgres.search import SearchVector
from django.db.models import F, Q
from apps.products.models import Product
import logging

logger = logging.getLogger('main')


def get_products_by_filter(request):
    try:
        word = request.data.get('word') or None
        min_price = request.data.get('min_price') or 0
        max_price = request.data.get('max_price') or 99999999999
        sorting = request.data.get('sorting') or '-id'
        category = request.data.get('category')
        subcategory = request.data.get('subcategory')

        products = Product.objects.showing_products().select_related('subcategory', "subcategory__category"). \
            annotate(discount_price=F('price') - (F('price') * F('discount') / 100)) \
            .filter(Q(discount_price__gte=min_price) & Q(discount_price__lte=max_price)).order_by(sorting)

        if category:
            products = products.filter(subcategory__category__slug=category)
        if subcategory:
            products = products.filter(subcategory__slug=subcategory)

        if word:
            products = Product.objects.annotate(
                search=SearchVector('title', 'subcategory__title', 'subcategory__category__title')
            ).filter(search=word)
            vector = SearchVector('title', weight='A') + SearchVector('subcategory__title', weight='B')
            vector += SearchVector('subcategory__category__title', weight='C')
            Product.objects.annotate(rank=SearchVector(vector, products)).order_by('rank')
        return products
    except Exception as ex:
        logger.error(ex)
        return []
