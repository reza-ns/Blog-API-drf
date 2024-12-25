from django.dispatch import receiver
from payment.signals import payment_success_signal
from django.utils import timezone
from . import models


@receiver(payment_success_signal)
def create_subscription(sender, payment, **kwargs):
    payment.purchase.status = models.Purchase.Status.PAID
    models.Subscription.objects.create(
        purchase=payment.purchase,
        start_time=timezone.now(),
        end_time=models.Plan.expiration_time_calculate(payment.purchase.plan),
    )


