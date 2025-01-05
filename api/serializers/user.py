from rest_framework import serializers
from adrf.serializers import ModelSerializer

from apps.users.models import CustomUser


class UserSerializer(ModelSerializer):
    cnt_comments = serializers.IntegerField(source='count_comments')

    class Meta:
        model = CustomUser
        fields = ("id", "email", "username", "slug", "cnt_comments")
