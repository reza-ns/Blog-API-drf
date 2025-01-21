from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from .managers import CustomUserManager


class User(AbstractBaseUser):
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
    username = models.CharField(max_length=128, unique=True, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=11, unique=True, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.role == self.ROLE_ADMIN:
            return True
        return False

