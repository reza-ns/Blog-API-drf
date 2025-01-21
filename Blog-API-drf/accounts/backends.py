from django.contrib.auth.backends import BaseBackend
from django.db.models import Q
from .models import User
from .utils.OTP_send import email_otp_verify, sms_otp_verify


class UsernameOrEmailOrPhoneBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        username = kwargs.get('username')
        email = kwargs.get('email')
        phone_number = kwargs.get('phone_number')
        password = kwargs.get('password')
        code = kwargs.get('code')

        if username is None and email is None and phone_number is None:
            return None
        if email or username:
            try:
                user = User.objects.get(Q(username=username)|Q(email=username))
                if password:
                    if user.check_password(password) and self.user_can_authenticate(user):
                        return user
                    else:
                        return None
                elif code:
                    if email_otp_verify(user.email, code) and self.user_can_authenticate(user):
                        return user
                    else:
                        return None
                else:
                    return None
            except User.DoesNotExist:
                print("UserDoesNotExist")
                return None
        elif phone_number:
            try:
                user = User.objects.get(phone_number=phone_number)
                if code:
                    if sms_otp_verify(phone_number, code) and self.user_can_authenticate(user):
                        return user
                    else:
                        return None
            except User.DoesNotExist:
                return None

    def  get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None

    def user_can_authenticate(self, user):
        return user.is_active
