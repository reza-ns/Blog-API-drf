from rest_framework.generics import RetrieveAPIView
from accounts.models import User
from . import serializers
from . import permissions


class UserView(RetrieveAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsUser,)
    queryset = User.objects.all()
    lookup_url_kwarg = 'user_id'