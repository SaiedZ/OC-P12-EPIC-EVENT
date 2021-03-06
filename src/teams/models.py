"""
Custom user and team models.
"""

from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import CustomAccountManager, UniqueNameManager


class CRMUser(AbstractBaseUser, PermissionsMixin):
    """The user of the EPICEVENT CRM."""

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format:"
        + " '+999999999'. Up to 15 digits allowed.")

    email = models.EmailField(_("email adress"), max_length=100, unique=True)
    username = models.CharField(_("username"), max_length=10, unique=True)
    first_name = models.CharField(max_length=25, blank=False)
    last_name = models.CharField(max_length=25, blank=False)
    phone = models.CharField(_("phone number"), max_length=20,
                             validators=[phone_regex], blank=True, null=True)
    mobile = models.CharField(_("mobile number"), max_length=20,
                              validators=[phone_regex], blank=True, null=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    team = models.ForeignKey(
        "Team", related_name="team", on_delete=models.SET_NULL, null=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = ("CRM User")
        verbose_name_plural = ("CRM Users")

    def __str__(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"


class Team(models.Model):
    """Represents the Team of the user."""

    name = models.CharField(
        _("Team name"),
        max_length=200,
        validators=[MinLengthValidator(2)],
        unique=True,
    )

    objects = UniqueNameManager()

    class Meta:
        ordering = ['name']
        verbose_name_plural = _("Teams")

    def __str__(self):
        return self.name

    def natural_key(self):
        """Returns the natural key used for fixture serialization."""
        return self.name
