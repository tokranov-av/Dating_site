from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    """Сериализатор, используемый при отображении списка пользователей."""
    match = serializers.HyperlinkedIdentityField(
        view_name='user_liked', read_only=True
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'gender', 'avatar', 'match',
        )


class UserCreateSerializer(BaseUserCreateSerializer):
    """Сериализатор, используемый при регистрации пользователей."""
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = (
            'email', 'first_name', 'last_name', 'gender', 'avatar',
            'latitude', 'longitude', 'password',
        )
