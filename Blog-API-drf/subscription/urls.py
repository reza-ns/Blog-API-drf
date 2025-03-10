from django.urls import path
from django.views.decorators.cache import cache_page
from subscription.api import views


app_name = 'subscription'

urlpatterns = [
    path('create/<int:plan_id>', views.PurchaseCreate.as_view(), name='purchase_create'),
    path('list', cache_page(1200, key_prefix='plan_list')(views.SubsPlanList.as_view()),
         name='subs_plans_list'),
]