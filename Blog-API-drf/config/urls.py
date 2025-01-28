from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('user/', include('accounts.urls', namespace='accounts')),
    path('subs/', include('subscription.urls', namespace='subscription')),
    path('pay/', include('payment.urls', namespace='payment')),
]
