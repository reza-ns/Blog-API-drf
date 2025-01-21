from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User
from accounts.utils.OTP_send import sms_otp_send, sms_otp_verify
from rest_framework.permissions import AllowAny
from . import serializers
from . import permissions


class UserView(RetrieveAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsUser,)
    queryset = User.objects.all()
    lookup_url_kwarg = 'user_id'


class AuthView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        # serializer = serializers.AuthSerializer(data=request.data)
        # if serializer.is_valid():
        #     data = serializer.validated_data
        #     username = data.get('username')
        #     email = data.get('email')
        #     phone_number = data.get('phone_number')
        #     password = data.get('password')
        #     if username:
        #         # user = User.objects.filter(username=username)
        #         # if not user.exists():
        #         #     user = User.objects.create(username=username, password=password)
        #         # user, created = User.objects.get_or_create(username=username, defaults={'password': password})
        #         user = User.objects.create_user(username, password=password)
        #     elif email:
        #         # user = User.objects.filter(email=email)
        #         # if not user.exists():
        #         #     user = User.objects.create(email=email, password=password)
        #         ...
        #     elif phone_number:
        #         sms_otp_send(phone_number)
        #         sms_otp_verify(phone_number, password)
        #         user = User.objects.filter(phone_number=phone_number)
        #
        #     refresh = RefreshToken.for_user(user)
        #     result = serializers.ObtainTokenSerializer({
        #         'refresh': str(refresh),
        #         'access': str(refresh.access_token)
        #     })
        #     return Response(result.data)
        ...
