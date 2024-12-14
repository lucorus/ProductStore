from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['title', 'slug', 'image']


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=False)

    class Meta:
        model = models.SubCategory
        fields = ['title', 'slug', 'image', 'category']


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url')
    estimation = serializers.DecimalField(source='get_estimation', decimal_places=2, max_digits=10)
    subcategory = SubCategorySerializer(many=False, read_only=True)

    class Meta:
        model = models.Product
        fields = ['title', 'slug', 'price', 'discount', 'photo', 'estimation', 'url', 'subcategory']


class CategoriesSerializer(serializers.ModelSerializer):
    # url = serializers.URLField(source='get_absolute_url')
    subcategories = SubCategorySerializer(many=True)

    class Meta:
        model = models.Category
        fields = ['title', 'slug', 'image', 'subcategories']
