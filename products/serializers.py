from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url')

    class Meta:
        model = models.Category
        fields = ['title', 'slug', 'image', 'url']


class SubCategorySerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url')
    category = CategorySerializer(many=False, read_only=False)

    class Meta:
        model = models.SubCategory
        fields = ['title', 'slug', 'image', 'url', 'category']


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url')
    subcategory = SubCategorySerializer(many=False, read_only=True)

    class Meta:
        model = models.Product
        fields = ['title', 'slug', 'price', 'discount', 'photo', 'url', 'subcategory']


class CategoriesSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url')
    subcategories = SubCategorySerializer(many=True)

    class Meta:
        model = models.Category
        fields = ['title', 'slug', 'image', 'url', 'subcategories']
