from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
import uuid
from subscription import models
from . import serializers
from payment.models import Payment


class PurchaseCreate(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None, *args, **kwargs):
        plan = get_object_or_404(models.Plan, id=self.kwargs.get('plan_id'))
        if plan.is_enable:
            payment = Payment.objects.create(user=request.user, amount=plan.price)
            models.Purchase.objects.create(user=request.user, plan=plan,
                                           price=plan.price, payment=payment)
            result = serializers.PlanRetrieveSerializer(plan)
            return Response(result.data)
        else:
            return Response({'Plan not found'}, status=status.HTTP_400_BAD_REQUEST)


class SubsPlanList(ListAPIView):
    queryset = models.Plan.objects.filter(is_enable=True)
    serializer_class = serializers.PlanRetrieveSerializer

