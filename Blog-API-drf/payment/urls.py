from django.urls import path
from payment.api import views


app_name = 'payment'

urlpatterns = [
    path('<uuid:payment_uid>', views.PaymentView.as_view(), name='payment'),
    path('verify', views.PaymentVerify.as_view(), name='payment_verify'),
]

