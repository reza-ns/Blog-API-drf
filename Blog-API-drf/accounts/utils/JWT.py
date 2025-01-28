from rest_framework_simplejwt.tokens import RefreshToken
from accounts.api.serializers import ObtainTokenSerializer


def create_jwt_tokens(user):
    refresh = RefreshToken.for_user(user)
    result = ObtainTokenSerializer({
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    })
    return result