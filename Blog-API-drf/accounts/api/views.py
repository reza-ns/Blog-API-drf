from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.conf import settings
import uuid
import redis
from accounts.models import User
from accounts.utils import OTP
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
        serializer = serializers.RegisterOTPSendSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            email = data.get('email')
            phone_number = data.get('phone_number')
            r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

            if email:
                if User.objects.filter(email=email).exists():
                    return Response({"A user with this email address already exists."},
                                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                otp_code = OTP.email_otp_send(email)
                request_id = uuid.uuid4()
                # Save email and otp_code and request_id in Redis with expire time(60 seconds)
                anonymous_user_data = {'code': otp_code, 'request_id': str(request_id)}
                r.hset(name=email, mapping=anonymous_user_data)
                r.expire(name=email, time=120, nx=True)

                return Response({'request_id': request_id})

            elif phone_number:
                if User.objects.filter(phone_number=phone_number).exists():
                    return Response({"A user with this phone number already exists."},
                                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                otp_code = OTP.sms_otp_send(phone_number)
                request_id = uuid.uuid4()
                # Save phone_number and otp_code and request_id in Redis with expire time(60 seconds)
                anonymous_user_data = {'code': otp_code, 'request_id': str(request_id)}
                r.hset(name=phone_number, mapping=anonymous_user_data)
                r.expire(name=phone_number, time=120, nx=True)

                return Response({'request_id': request_id})
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = serializers.RegisterOTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            email = data.get('email')
            phone_number = data.get('phone_number')
            code = data.get('code')
            request_id = data.get('request_id')
            r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

            if email:
                # Check if given email and request_id and code exist in Redis
                # If yes compare given data with redis saved data and create user
                # if no return error
                if r.exists(email) == 1:
                    request_id = r.hget(email, str(request_id))
                    code = r.hget(email, code)
                    if request_id == request_id and code==code:
                        user = User.objects.create_user(email=email)
                        result = self.create_jwt_tokens(user)
                        return Response(result.data)
                return Response(status=status.HTTP_400_BAD_REQUEST)

            elif phone_number:
                # Check if given phone_number and request_id and code exist in Redis
                # If yes ---> compare given data with redis saved data and create user
                # if no ---> return error
                if r.exists(phone_number) == 1:
                    request_id = r.hget(phone_number, str(request_id))
                    code = r.hget(phone_number, code)
                    if request_id == request_id and code==code:
                        user = User.objects.create_user(phone_number=phone_number)
                        result = self.create_jwt_tokens(user)
                        return Response(result.data)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def create_jwt_tokens(user):
        refresh = RefreshToken.for_user(user)
        result = serializers.ObtainTokenSerializer({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })
        return result


class UserLoginView(APIView):
    ...
