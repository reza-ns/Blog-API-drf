from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.conf import settings
from django.contrib.auth import authenticate
import uuid
from accounts.models import User
from accounts.utils import OTP, JWT, Redis
from . import serializers
from . import permissions


class UserView(RetrieveAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsUser,)
    queryset = User.objects.all()
    lookup_url_kwarg = 'user_id'


class UserRegisterView(APIView):
    permission_classes = (AllowAny,)
    expire_time = settings.REDIS_EXPIRE_TIME

    def get(self, request, format=None):
        """
        Get email or phone number
        save it with request id and otp code in Redis
        return a token as request id
        """
        serializer = serializers.RegisterOTPSendSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            email = data.get('email')
            phone_number = data.get('phone_number')

            if email:
                if User.objects.filter(email=email).exists():
                    return Response({"A user with this email address already exists."},
                                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                otp_code = OTP.email_otp_send(email)
                request_id = uuid.uuid4()
                anonymous_user_data = {'email': email, 'code': otp_code}
                Redis.redis_save(name=str(request_id), dic=anonymous_user_data,
                                 expire_time=self.expire_time)
                return Response({'request_id': request_id})

            elif phone_number:
                if User.objects.filter(phone_number=phone_number).exists():
                    return Response({"A user with this phone number already exists."},
                                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                otp_code = OTP.sms_otp_send(phone_number)
                request_id = uuid.uuid4()
                anonymous_user_data = {'phone_number': phone_number, 'code': otp_code}
                Redis.redis_save(name=str(request_id), dic=anonymous_user_data,
                                 expire_time=self.expire_time)
                return Response({'request_id': request_id})
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def post(self, request, format=None):
        """
        Check if given request_id and code exist in Redis
        If yes, compare given data with redis saved data and create user
        if no, return error
        """
        serializer = serializers.RegisterOTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            otp_code = data.get('code')
            request_id = str(data.get('request_id'))

            expire_status, user_data= Redis.redis_get(name=request_id)
            if expire_status:
                code = user_data.get('code')
                if code == otp_code:
                    if 'email' in user_data:
                        email = user_data.get('email')
                        user = User.objects.create_user(email=email)
                        result = JWT.create_jwt_tokens(user)
                        return Response(result.data)
                    elif 'phone_number' in user_data:
                        phone_number = user_data.get('phone_number')
                        user = User.objects.create_user(phone_number=phone_number)
                        result = JWT.create_jwt_tokens(user)
                        return Response(result.data)
                return Response({"Code is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    expire_time = settings.REDIS_EXPIRE_TIME

    def get(self, request, format=None):
        serializer = serializers.LoginOTPSendSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            username = data.get('username')
            email = data.get('email')
            phone_number = data.get('phone_number')

            request_id = uuid.uuid4()
            if username:
                if not User.objects.filter(username=username).exists():
                    return Response({"User with this username does not exist"},
                                    status=status.HTTP_404_NOT_FOUND)
                anonymous_user_data = {'username': username}
                Redis.redis_save(name=str(request_id), dic=anonymous_user_data,
                                 expire_time=3600)
                return Response({'request_id': request_id})

            elif email:
                if not User.objects.filter(email=email).exists():
                    return Response({"User with this email does not exist"},
                                    status=status.HTTP_404_NOT_FOUND)
                otp_code = OTP.email_otp_send(email)
                anonymous_user_data = {'email': email, 'code': otp_code}
                Redis.redis_save(name=str(request_id), dic=anonymous_user_data,
                                 expire_time=self.expire_time)
                return Response({'request_id': request_id})

            elif phone_number:
                if not User.objects.filter(phone_number=phone_number).exists():
                    return Response({"User with this phone number does not exist"},
                                    status=status.HTTP_404_NOT_FOUND)
                otp_code = OTP.sms_otp_send(phone_number)
                anonymous_user_data = {'phone_number': phone_number, 'code': otp_code}
                Redis.redis_save(name=str(request_id), dic=anonymous_user_data,
                                 expire_time=self.expire_time)
                return Response({'request_id': request_id})
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def post(self, request, format=None):
        serializer = serializers.LoginOTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            request_id = str(data.get('request_id'))
            otp_code = data.get('code')
            password = data.get('password')

            user = authenticate(request_id=request_id, otp=otp_code, password=password)
            if user is not None:
                result = JWT.create_jwt_tokens(user)
                return Response(result.data)
            return Response({"Invalid code or password"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)



