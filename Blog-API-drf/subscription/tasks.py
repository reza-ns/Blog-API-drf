from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task()
def subscription_expiration(subscription):
    subscription.is_active = False
    subscription.user.role = User.UserRole.MEMBER
    subscription.save()
