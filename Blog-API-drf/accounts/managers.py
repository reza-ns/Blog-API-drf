from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None):
        if email is None and phone_number is None:
            raise ValueError('User must have email or phone number')
        user = self.model(email=self.normalize_email(email),phone_number=phone_number)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, email=None, phone_number=None):
        user = self.create_user(email, phone_number, password)
        user.role = self.model.ROLE_ADMIN
        user.save(using=self._db)
        return user
