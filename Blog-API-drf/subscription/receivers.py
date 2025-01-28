from django.dispatch import receiver
from payment.signals import payment_success_signal
from django.utils import timezone
from . import models
from .tasks import subscription_expiration
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(payment_success_signal)
def create_subscription(sender, payment, **kwargs):
    payment.purchase.status = models.Purchase.Status.PAID
    subscription = models.Subscription.objects.create(
        purchase=payment.purchase,
        user=payment.user,
        start_time=timezone.now(),
        end_time=models.Plan.expiration_time_calculate(payment.purchase.plan),
    )
    payment.user.role = User.UserRole.SUBSCRIBER
    subscription_expiration(subscription).apply_async(eta=subscription.end_time)



