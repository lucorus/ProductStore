from rest_framework import serializers
from adrf.serializers import ModelSerializer

from .products import ProductSerializer
from apps.basket.models import Basket


class BasketSerializer(ModelSerializer):
    product = ProductSerializer(read_only=True)
    get_count_products = serializers.IntegerField(source="get_count_products_in_basket")
    get_sum = serializers.IntegerField(source="get_sum_products")

    class Meta:
        model = Basket
        fields = ['id', 'product', 'count', 'created_at', "get_sum", "get_count_products"]
