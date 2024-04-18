from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    subcategory_title = serializers.CharField(source='subcategory.title')
    subcategory_slug = serializers.CharField(source='subcategory.slug')
    category_title = serializers.CharField(source='subcategory.category.title')
    category_slug = serializers.CharField(source='subcategory.category.slug')
    url = serializers.CharField(source='get_absolute_url')
    category_url = serializers.CharField(source='subcategory.category.get_absolute_url')
    subcategory_url = serializers.CharField(source='subcategory.get_absolute_url')

    class Meta:
        model = Product
        fields = ['title', 'slug', 'price', 'discount', 'photo',
                  'subcategory_title', 'subcategory_slug', 'category_title',
                  'category_slug', 'url', 'category_url', 'subcategory_url']
