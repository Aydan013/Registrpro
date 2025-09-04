# serializers.py
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *


CustomerUser = get_user_model()

class CustomerUserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomerUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        extra_kwargs = {
            'password1': {'write_only': True},
            'password2': {'write_only': True},
        }

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password2": "Password fields didn't match."})
        
        try:
            validate_password(data['password1'])
        except ValidationError as e:
            raise serializers.ValidationError({'password1': list(e.messages)})
            
        return data

    def create(self, validated_data):
        user = CustomerUser.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password1']
        )
        return user


        fields = ["id", "username", "first_name", "last_name", "email"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ['username', 'first_name', 'last_name', 'email']

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("İstifadəçi adı və şifrə tələb olunur")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Yanlış istifadəçi adı və ya şifrə")
        if not user.is_active:
            raise serializers.ValidationError("Bu hesab deaktiv edilib")

        data['user'] = user
        return data



class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser

# User məlumatlarını göstərmək üçün
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

# User məlumatlarını yeniləmək üçün
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ['username', 'first_name', 'last_name', 'email']
        
    def validate_username(self, value):
        # İstifadəçi adının unikal olmasını yoxlayırıq, amma cari istifadəçini istisna edirik
        user = self.context['request'].user
        if CustomerUser.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value
        
    def validate_email(self, value):
        # Email-in unikal olmasını yoxlayırıq, amma cari istifadəçini istisna edirik
        user = self.context['request'].user
        if CustomerUser.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

# Login üçün serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            
            if not user:
                raise serializers.ValidationError("Yanlış istifadəçi adı və ya şifrə")
            if not user.is_active:
                raise serializers.ValidationError("Bu hesab deaktiv edilib")
                
        else:
            raise serializers.ValidationError("İstifadəçi adı və şifrə tələb olunur")
            
        data['user'] = user
        return data