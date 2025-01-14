from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('user/', include('accounts.urls', namespace='accounts')),
    path('subs/', include('subscription.urls', namespace='subscription')),
    path('pay/', include('payment.urls', namespace='payment')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
