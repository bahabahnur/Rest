from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

USER_TYPE_CHOICES = (
    ('owner', 'Owner'),
    ('customer', 'Customer'),
    )


class RegisterAPISerializer(serializers.ModelSerializer):
    """Создание сериализации для RegisterAPIView"""
    password = serializers.CharField(
        min_length=8, required=True,
        write_only=True, )
    password_confirmation = serializers.CharField(
        min_length=8, required=True,
        write_only=True, )
    user_type = serializers.ChoiceField(choices=USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ("email", "password",
                  "password_confirmation",
                  "user_type")

    """Проверка на email"""
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Уже существует!!!")
        return value

    """Проверка на совпадение пароля. И через поп удаляем password_confirmation"""
    def validate(self, attrs):
        password = attrs.get("password")
        password_confirmation = attrs.pop("password_confirmation")

        if password != password_confirmation:
            raise serializers.ValidationError("Пароль не совпадают")
        return attrs

    """Попадает конечные данные"""
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
