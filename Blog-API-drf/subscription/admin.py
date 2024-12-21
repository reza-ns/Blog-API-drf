from django.contrib import admin
from . import models


class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_enable')


class PurchaseAdmin(admin.ModelAdmin):
    ...


class SubscriptionAdmin(admin.ModelAdmin):
    ...


admin.site.register(models.Plan, PlanAdmin)
admin.site.register(models.Purchase, PurchaseAdmin)
admin.site.register(models.Subscription, SubscriptionAdmin)

