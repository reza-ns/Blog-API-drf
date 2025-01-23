from rest_framework import serializers
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RegisterOTPSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'phone_number')


class RegisterOTPVerifySerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=10)
    request_id = serializers.UUIDField(format='hex_verbose')
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'code', 'request_id')


class ObtainTokenSerializer(serializers.Serializer):
    access = serializers.CharField(max_length=128, allow_null=False)
    refresh = serializers.CharField(max_length=128, allow_null=False)
