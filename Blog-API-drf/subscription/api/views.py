from rest_framework.generics import ListAPIView
from subscription.models import Plan
from . import serializers


class SubsPlanList(ListAPIView):
    queryset = Plan.objects.filter(is_enable=True)
    serializer_class = serializers.PlanRetrieveSerializer