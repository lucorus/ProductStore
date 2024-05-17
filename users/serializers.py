from products.serializers import ProductSerializer
from rest_framework import serializers
from . import models


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ['id', 'username', 'slug']


class CommentSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(many=False, read_only=True)
    # product = ProductSerializer(many=False, read_only=True)
    cnt_answers = serializers.IntegerField(source='count_answers')
    # answers = serializers.ListField(source='get_answers')

    class Meta:
        model = models.Comment
        fields = ['id', 'author', 'text', 'estimation', 'cnt_answers']
