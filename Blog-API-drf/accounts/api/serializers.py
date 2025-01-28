from rest_framework import serializers
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'date_joined')


class RegisterOTPSendSerializer(serializers.Serializer):
    email = serializers.EmailField(default=None)
    phone_number = serializers.CharField(max_length=11, default=None)


class RegisterOTPVerifySerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=10)
    request_id = serializers.UUIDField(format='hex_verbose')
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'code', 'request_id')


class LoginOTPSendSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128, default=None)
    email = serializers.EmailField(default=None)
    phone_number = serializers.CharField(max_length=11, default=None)


class LoginOTPVerifySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=10, required=False)
    request_id = serializers.UUIDField(format='hex_verbose')
    password = serializers.CharField(max_length=128, default=None)


class ObtainTokenSerializer(serializers.Serializer):
    access = serializers.CharField(max_length=128, allow_null=False)
    refresh = serializers.CharField(max_length=128, allow_null=False)
