from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager

from .enums import Role


class UserManager(BaseUserManager):
    def create_user(
        self, email: str, password: str | None = None, **extra_field
    ):  # noqa
        user = self.model(email=self.normalize_email(email), **extra_field)  # noqa
        setattr(user, "password", make_password(password))
        user.save()  # we will use using=self._db inside parentheses only when we have many other db for save inf # noqa
        # user.password = make_password(password)
        return user

    def create_superuser(
        self, email: str, password: str | None = None, **extra_field
    ):  # noqa
        return self.create_user(
            email=email,
            password=password,
            role=Role.SENIOR,
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
