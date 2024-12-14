from rest_framework import serializers

from apps.users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    cnt_comments = serializers.IntegerField(source='count_comments')

    class Meta:
        model = CustomUser
        fields = ("id", "email", "username", "slug", "cnt_comments")
