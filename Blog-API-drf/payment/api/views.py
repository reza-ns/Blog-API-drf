from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import redirect, get_object_or_404
from django.conf import settings
from payment.models import Payment
from payment.utils import zarinpal
from . import serializers
from .permissions import IsPaymentOwner
from payment.signals import payment_success_signal


class PaymentView(APIView):
    permission_classes = (IsAuthenticated, IsPaymentOwner)

    def get(self, request, format=None):
        payment = get_object_or_404(Payment, uid=request.query_params.get('payment_uid'))
        self.check_object_permissions(request, payment)
        payment_link, authority = zarinpal.zpal_payment_request(
                                    merchant_id=settings.ZARINPAL['merchant_id'],
                                    amount=payment.amount,
                                    description='buy subscription',
                                    user_email=request.user.email,
                                    user_phone=None,
                                    callback_url= settings.ZARINPAL['callback_url']
                                    )
        if authority:
            payment.authority = authority
            payment.save()
            return redirect(payment_link)
        else:
            payment.status = Payment.STATUS.FAILED
            payment.save()
            return Response({'Payment failed'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class PaymentVerify(APIView):
    permission_classes = (IsAuthenticated, IsPaymentOwner)

    def get(self, request, format=None):
        authority = request.query_params.get('Authority')
        payment = get_object_or_404(Payment, authority=authority)
        self.check_object_permissions(request, payment)
        if request.query_params.get('Status') == 'OK':
            is_paid, ref_id = zarinpal.zpal_payment_verify(
                                    merchant_id=settings.ZARINPAL['merchant_id'],
                                    authority=payment.authority,
                                    amount=payment.amount
                                    )
            if is_paid:
                payment.ref_id = ref_id
                payment.status = Payment.STATUS.SUCCESS
                payment.save()

                payment_success_signal.send(sender=payment, payment=payment)

                result = serializers.PaymentSerializer(payment)
                return Response(result.data)
            else:
                payment.status = Payment.STATUS.FAILED
                payment.save()
                return Response({'Payment failed'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        elif request.query_params.get('Status') == 'NOK':
            payment.status = Payment.STATUS.FAILED
            payment.save()
            return Response({'Payment failed'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)