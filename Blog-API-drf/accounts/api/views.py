from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.conf import settings
import uuid
import redis
from accounts.models import User
from accounts.utils import OTP, JWT
from . import serializers
from . import permissions


class UserView(RetrieveAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsUser,)
    queryset = User.objects.all()
    lookup_url_kwarg = 'user_id'


class UserRegisterView(APIView):
    permission_classes = (AllowAny,)

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
            r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB,
                            charset="utf-8", decode_responses=True)

            if email:
                if User.objects.filter(email=email).exists():
                    return Response({"A user with this email address already exists."},
                                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                otp_code = OTP.email_otp_send(email)
                request_id = uuid.uuid4()
                anonymous_user_data = {'email': email, 'code': otp_code}
                r.hset(name=str(request_id), mapping=anonymous_user_data)
                r.expire(name=str(request_id), time=120, nx=True)
                return Response({'request_id': request_id})

            elif phone_number:
                if User.objects.filter(phone_number=phone_number).exists():
                    return Response({"A user with this phone number already exists."},
                                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                otp_code = OTP.sms_otp_send(phone_number)
                request_id = uuid.uuid4()
                anonymous_user_data = {'phone_number': phone_number, 'code': otp_code}
                r.hset(name=str(request_id), mapping=anonymous_user_data)
                r.expire(name=str(request_id), time=120, nx=True)
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

            r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB,
                            charset="utf-8", decode_responses=True)
            if r.exists(request_id) == 1:
                code = r.hget(request_id, 'code')
                if otp_code == code:
                    if r.hexists(name=request_id, key='email'):
                        email = r.hget(request_id, 'email')
                        user = User.objects.create_user(email=email)
                        result = JWT.create_jwt_tokens(user)
                        return Response(result.data)
                    elif r.hexists(name=request_id, key='phone_number'):
                        phone_number = r.hget(request_id, 'phone_number')
                        user = User.objects.create_user(phone_number=phone_number)
                        result = JWT.create_jwt_tokens(user)
                        return Response(result.data)
                return Response({"Code is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class UserLoginView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        serializer = serializers.LoginOTPSendSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            username = data.get('username')
            email = data.get('email')
            phone_number = data.get('phone_number')
            r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB,
                            charset="utf-8", decode_responses=True)
            request_id = uuid.uuid4()
            if username:
                if not User.objects.filter(username=username).exists():
                    return Response({"User with this username does not exist"},
                                    status=status.HTTP_404_NOT_FOUND)
                r.hset(name=str(request_id), key='username', value=username)
                r.expire(name=str(request_id), time=3600, nx=True)
                return Response({'request_id': request_id})

            elif email:
                if not User.objects.filter(email=email).exists():
                    return Response({"User with this email does not exist"},
                                    status=status.HTTP_404_NOT_FOUND)
                otp_code = OTP.email_otp_send(email)
                anonymous_user_data = {'email': email, 'code': otp_code}
                r.hset(name=str(request_id), mapping=anonymous_user_data)
                r.expire(name=str(request_id), time=120, nx=True)
                return Response({'request_id': request_id})

            elif phone_number:
                if not User.objects.filter(phone_number=phone_number).exists():
                    return Response({"User with this phone number does not exist"},
                                    status=status.HTTP_404_NOT_FOUND)
                otp_code = OTP.sms_otp_send(phone_number)
                anonymous_user_data = {'phone_number': phone_number, 'code': otp_code}
                r.hset(name=str(request_id), mapping=anonymous_user_data)
                r.expire(name=str(request_id), time=120, nx=True)
                return Response({'request_id': request_id})
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def post(self, request, format=None):
        serializer = serializers.LoginOTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            otp_code = data.get('code')
            request_id = str(data.get('request_id'))
            password = data.get('password')

            r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB,
                            charset="utf-8", decode_responses=True)
            if r.exists(request_id) == 1:
                code = r.hget(request_id, 'code')
                if otp_code == code:
                    if r.hexists(name=request_id, key='username') and password:
                        username = r.hget(request_id, 'username')
                        user = User.objects.get(username=username)
                        if user.check_password(password):
                            result = JWT.create_jwt_tokens(user)
                            return Response(result.data)
                        return Response({"Password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

                    elif r.hexists(name=request_id, key='email'):
                        email = r.hget(request_id, 'email')
                        user = User.objects.get(email=email)
                        result = JWT.create_jwt_tokens(user)
                        return Response(result.data)

                    elif r.hexists(name=request_id, key='phone_number'):
                        phone_number = r.hget(request_id, 'phone_number')
                        user = User.objects.get(phone_number=phone_number)
                        result = JWT.create_jwt_tokens(user)
                        return Response(result.data)
                return Response({"Code is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

