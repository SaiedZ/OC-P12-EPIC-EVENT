from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    """Client model."""

    first_name = models.CharField(_("first name"), max_length=25)
    last_name = models.CharField(_("last name"), max_length=25)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(_("phone number"), max_length=20,
                             blank=True, null=True)
    mobile = models.CharField(_("mobile number"), max_length=20,
                              blank=True, null=True)
    compagny_name = models.CharField(_("compagny name"), max_length=250,
                                     unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """string representation of a client representing the compagny_name."""
        return f"{self.compagny_name.capitalize()}"
