from rest_framework import serializers

from .products import ProductSerializer
from .user import UserSerializer
from apps.users.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    comment_author = UserSerializer(read_only=True)
    product_commented = ProductSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "comment_author", "product_commented", "text", "estimation"]
