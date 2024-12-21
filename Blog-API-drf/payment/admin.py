from django.contrib import admin
from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    ...


admin.site.register(Payment, PaymentAdmin)