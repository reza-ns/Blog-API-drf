from rest_framework import serializers
from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('amount', 'ref_id', 'status')