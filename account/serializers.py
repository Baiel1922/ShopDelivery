from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from .models import MyUser, InfoUser
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
            raise serializers.ValidationError('User is not found')
        return email

    def validate_code(self, code):
        if not MyUser.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Activation code not found')
        return code


    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('activation_code')
        if not MyUser.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError('Activation code not found')
        return attrs

    def activate(self):
        email = self.validated_data.get('email')
        user = MyUser.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label='password',
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                messege = "Unable to log in with provided credentials"
                raise serializers.ValidationError(messege, code='authorization')

        else:
            messege = "Must include 'email' and 'password'."
            raise serializers.ValidationError(messege, code="authorization")

        attrs['user'] = user
        return attrs

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)
    new_password_confirm = serializers.CharField(required=True, min_length=6)

    def validate_old_password(self, old_password):
        user = self.context.get("request").user
        if not user.check_password(old_password):
            raise serializers.ValidationError("Incorrect password")
        return old_password

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        new_password_confirm = attrs.get("new_password_confirm")

        if new_password != new_password_confirm:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def set_new_password(self):
        user = self.context.get('request').user
        password = self.validated_data.get('new_password')
        user.set_password(password)
        user.save()

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not MyUser.objects.filter(email=email):
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def send_code(self):
        email = self.validated_data.get('email')
        user = MyUser.objects.get(email=email)
        user.create_activation_code()
        send_activation_code(email=user.email, activation_code=user.activation_code)

class ForgetPasswordCompleteSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)
    activation_code = serializers.CharField(min_length=6, required=True)

    def validate_email(self, email):
        if not MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не зарегистрирован')
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают')

        code = attrs.get('activation_code')
        if not MyUser.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Неверный активационный код')
        return attrs

    def set_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = MyUser.objects.get(email=email)
        user.set_password(password)
        user.activation_code = ''
        user.save()

class InfoUserSerializer(serializers.ModelSerializer):
    author = ReadOnlyField(source='author.email')

    class Meta:
        model = InfoUser
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        info, _ = InfoUser.objects.update_or_create(
            author=user,
            defaults={'name': validated_data.get('name'),
                      'surname': validated_data.get('surname'),
                      'phone': validated_data.get('phone'),
                      'image': validated_data.get('image')
                      }
        )

        return info