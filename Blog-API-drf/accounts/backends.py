from django.contrib.auth.backends import BaseBackend
from django.db.models import Q
from .models import User


class UsernameOrEmailBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        username = kwargs.get('username')
        email = kwargs.get('email')
        password = kwargs.get('password')

        if username is None and email is None:
            return None
        if email or username:
            try:
                user = User.objects.get(Q(username=username)|Q(email=username))
                if user.check_password(password) and self.user_can_authenticate(user):
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
