from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, first_name,
                         last_name, password, **other_fields):

        other_fields.setdefault("is_superuser", True)

        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True")

        return self.create_user(email, username, first_name,
                                last_name, password, **other_fields)

    def create_user(self, email, username, first_name,
                    last_name, password, **other_fields):

        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          first_name=first_name, last_name=last_name,
                          **other_fields)
        user.set_password(password)
        user.save()

        return user


class CRMUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_("email adress"), max_length=100, unique=True)
    username = models.CharField(_("username"), max_length=10, unique=True)
    first_name = models.CharField(max_length=25, blank=False)
    last_name = models.CharField(max_length=25, blank=False)
    phone = models.CharField(_("phone number"), max_length=20,
                             blank=True, Null=True)
    mobile = models.CharField(_("mobile number"), max_length=20,
                              blank=True, Null=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"
