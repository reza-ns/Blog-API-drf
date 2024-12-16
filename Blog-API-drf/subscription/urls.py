from django.urls import path
from subscription.api.views import SubsPlanList


app_name = 'subscription'

urlpatterns = [
    path('list', SubsPlanList.as_view(), name='subs_plan_list'),
]