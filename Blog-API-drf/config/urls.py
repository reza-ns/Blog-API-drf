from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('blog/api/', include('blog.urls', namespace='blog')),
    path('user/api/', include('accounts.urls', namespace='accounts')),
    path('subs/api/', include('subscription.urls', namespace='subscription')),
    path('pay/api/', include('payment.urls', namespace='payment')),
]
