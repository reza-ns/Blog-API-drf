from django.contrib.auth.models import BaseUserManager
import random


class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None):
        if email is None and phone_number is None:
            raise ValueError('User must have email or phone number')

        email = None if email is None else self.normalize_email(email)
        user = self.model(
            email=email,
            phone_number=phone_number,
            username=self._generate_username(email, phone_number)
        )
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, email=None, phone_number=None):
        user = self.create_user(email, phone_number, password)
        user.role = self.model.UserRole.SUPERUSER
        user.save(using=self._db)
        return user

    @staticmethod
    def _generate_username(email=None, phone_number=None):
        if email:
            name = email.split('@')[0]
            username = f"{name}.{random.randint(1000, 9998)}"
            return username
        elif phone_number:
            username = f"{phone_number}.{random.randint(1000, 9998)}"
            return username
