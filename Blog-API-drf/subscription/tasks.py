from celery import shared_task


@shared_task()
def subscription_expiration(subscription):
    subscription.is_active = False
