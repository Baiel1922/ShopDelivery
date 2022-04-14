from rest_framework import serializers

from .models import MyUser
from .utils import send_activation_code

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirm = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'password', 'password_confirm']

    def validate(self, validated_data):
        password = validated_data.get("password")
        password_confirm = validated_data.get("password_confirm")
        if password != password_confirm:
            raise serializers.ValidationError('passwords do not match!!')
        return validated_data

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = MyUser.objects.create_user(email=email, password=password)
        send_activation_code(email=user.email, activation_code=user.activation_code)
        return user

class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    activation_code = serializers.CharField(min_length=8, max_length=100)

    def validate_email(self, email):
        if not MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не зарегистрирован')
        return email

    def validate_code(self, code):
        if not MyUser.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Активационный код не найден!')
        return code


    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('activation_code')
        if not MyUser.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError('Активационный код не найден')
        return attrs

    def activate(self):
        email = self.validated_data.get('email')
        user = MyUser.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()
