from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_AUTHOR = 'author'
    ROLE_ADMIN = 'admin'
    ROLE_SUBSCRIBER = 'subscriber'
    ROLE_MEMBER = 'member'

    ROLE_CHOICES = (
        (ROLE_AUTHOR, 'Author'),
        (ROLE_ADMIN, 'Admin'),
        (ROLE_SUBSCRIBER, 'Subscriber'),
        (ROLE_MEMBER, 'Member'),
    )

    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default=ROLE_MEMBER)