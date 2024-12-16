from django.db import models
from django.contrib.auth import  get_user_model

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


# class Subscription(models.Model):
#     plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
#     user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='subscriptions')
#     created_time = models.DateTimeField(auto_now_add=True)
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     is_active = models.BooleanField(default=True)
#
#     def __str__(self):
#         return f"{self.user} >> {self.plan.name}"
#
#
# class Purchase(models.Model):
#     class Status(models.IntegerChoices):
#         PAID = (10, 'Paid'),
#         NOT_PAID = (-10, 'Not Paid')
#
#     subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT, related_name='purchases')
#     payment = models.ForeignKey(Payment, on_delete=models.PROTECT, related_name='subscriptions')
#     price = models.PositiveBigIntegerField()
#     status = models.IntegerField(choices=Status.choices, default=Status.NOT_PAID)
#     created_time = models.DateTimeField(auto_now_add=True)
#     modified_time = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.subscription


