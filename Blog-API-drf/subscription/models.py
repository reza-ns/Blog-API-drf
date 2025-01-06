from django.db import models
from django.contrib.auth import  get_user_model
from django.utils import timezone
from payment.models import Payment


User = get_user_model()


class Plan(models.Model):
    class TimeUnit(models.TextChoices):
        DAY = ('D', 'Day')
        WEEK = ('W', 'Week')
        MONTH = ('M', 'Month')
        YEAR = ('Y', 'Year')

    name = models.CharField(max_length=100)
    price = models.PositiveBigIntegerField()
    description = models.TextField(null=True, blank=True)
    is_enable = models.BooleanField(default=True)
    time_unit = models.CharField(max_length=1, choices=TimeUnit.choices, default=TimeUnit.DAY)
    time_value = models.PositiveSmallIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def expiration_time_calculate(self):
        current_time = timezone.now()
        if self.time_unit == self.TimeUnit.YEAR:
            days = self.time_value * 365
            return current_time + timezone.timedelta(days=days)
        elif self.time_unit == self.TimeUnit.MONTH:
            days = self.time_value * 30
            return current_time + timezone.timedelta(days=days)
        elif self.time_unit == self.TimeUnit.WEEK:
            weeks = self.time_value
            return current_time + timezone.timedelta(weeks=weeks)
        else:
            days = self.time_value
            return current_time + timezone.timedelta(days=days)


class Purchase(models.Model):
    class Status(models.IntegerChoices):
        PAID = 10, 'Paid'
        NOT_PAID = -10, 'Not Paid'

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='purchases')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='purchases')
    payment = models.OneToOneField(Payment, on_delete=models.PROTECT, related_name='purchase')
    price = models.PositiveBigIntegerField()
    status = models.IntegerField(choices=Status.choices, default=Status.NOT_PAID)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}"


class Subscription(models.Model):
    purchase = models.OneToOneField(Purchase, on_delete=models.PROTECT, related_name='subscriptions')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='subscriptions')
    created_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.purchase}"





