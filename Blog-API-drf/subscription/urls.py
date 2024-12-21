from django.urls import path
from subscription.api import views


app_name = 'subscription'

urlpatterns = [
    path('create/<int:plan_id>', views.PurchaseCreate.as_view(), name='purchase_create'),
    path('list', views.SubsPlanList.as_view(), name='subs_plans_list'),
]