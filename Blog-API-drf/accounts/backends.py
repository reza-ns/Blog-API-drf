from django.contrib.auth.backends import BaseBackend
from django.db.models import Q
from .utils import Redis
from .models import User


class UsernameOrEmailBackend(BaseBackend):
    def authenticate(self, request, request_id=None, otp=None, password=None, **kwargs):
        if request_id is None and otp is None and password is None:
            return None

        username = kwargs.get('username')
        if username and password:
            try:
                user = User.objects.get(username=username)
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user
                return None
            except User.DoesNotExist:
                return None

        expire_status, user_data = Redis.redis_get(name=request_id)
        if expire_status:
            if 'username' in user_data and password:
                username = user_data.get('username')
                try:
                    user = User.objects.get(username=username)
                    if user.check_password(password) and self.user_can_authenticate(user):
                        return user
                    return None
                except User.DoesNotExist:
                    return None
            elif 'email' in user_data or 'phone_number' in user_data:
                email = user_data.get('email')
                phone_number = user_data.get('phone_number')
                try:
                    user = User.objects.get(Q(email=email) | Q(phone_number=phone_number))
                    code = user_data.get('code')
                    if code == otp and self.user_can_authenticate(user):
                        return user
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
