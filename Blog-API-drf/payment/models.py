from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Payment(models.Model):
    class STATUS(models.TextChoices):
        PENDING = ('pending', 'Pending')
        SUCCESS = ('success', 'Success')
        FAILED = ('failed', 'Failed')

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payments')
    amount = models.PositiveBigIntegerField()
    authority = models.CharField(max_length=100, null=True, blank=True)
    ref_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=7, choices=STATUS.choices, default=STATUS.PENDING)

    def __str__(self):
        return self.id
