from rest_framework import serializers
from users.models import User

class UserModelSerializer(serializers.ModelSerializer):
    """Сериализатор модели User, хэширует пароль."""
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "email", "password", "phone", "city", "avatar")
        read_only_fields = ("id",)

    def create(self, validated_data):
        """Хэшируем пароль перед сохранением."""
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)