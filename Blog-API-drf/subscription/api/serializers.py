from rest_framework import serializers
from subscription.models import Plan


class PlanRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('name', 'price', 'description')

