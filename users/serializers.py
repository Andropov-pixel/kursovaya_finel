from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            phone_number=validated_data.get("phone", ""),
            avatar=validated_data.get("avatar", None),
        )
        # Устанавливаем пароль пользователя
        user.set_password(validated_data["password"])
        user.save()
        return user