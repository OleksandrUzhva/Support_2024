from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(
        self, email: str, password: str | None = None, **extra_field
    ):  # noqa
        user = self.model(email=self.normalize_email(email), **extra_field)  # noqa
        setattr(user, "password", make_password(password))
        user.save()  # we will use using=self._db inside parentheses only when we have many other db for save inf # noqa
        # user.password = make_password(password)
        return user

    def creat_superuser(
        self, email: str, password: str | None = None, **extra_field
    ):  # noqa
        pass
