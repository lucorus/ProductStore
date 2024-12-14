from rest_framework import serializers

from apps.products.models import Product, Category, SubCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'slug', 'image']


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=False)

    class Meta:
        model = SubCategory
        fields = ['title', 'slug', 'image', 'category']


class ProductSerializer(serializers.ModelSerializer):
    # url = serializers.CharField(source='get_absolute_url')
    estimation = serializers.DecimalField(source='get_estimation', decimal_places=2, max_digits=10)
    subcategory = SubCategorySerializer(many=False, read_only=True)

    class Meta:
        model = Product
        fields = ['title', 'slug', 'price', 'discount', 'photo', 'estimation', 'subcategory']


class CategoriesSerializer(serializers.ModelSerializer):
    # url = serializers.URLField(source='get_absolute_url')
    subcategories = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['title', 'slug', 'image', 'subcategories']
