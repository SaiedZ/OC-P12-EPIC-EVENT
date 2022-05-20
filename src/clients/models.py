from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save

from contracts.models import Contract


class Client(models.Model):
    """Client model."""

    first_name = models.CharField(_("first name"), max_length=25)
    last_name = models.CharField(_("last name"), max_length=25)
    email = models.EmailField(max_length=100, unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format:"
        + " '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(_("phone number"), max_length=20,
                             validators=[phone_regex], blank=True, null=True)
    mobile = models.CharField(_("mobile number"), max_length=20,
                              validators=[phone_regex], blank=True, null=True)
    compagny_name = models.CharField(_("compagny name"), max_length=250,
                                     unique=True)
    potential = models.BooleanField(_("potential client"), default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """string representation of a client representing the compagny_name."""
        return f"{self.compagny_name.capitalize()}"


@receiver(post_save, sender=Contract)
def update_client_from_potential_to_existant(sender, instance, *args, **kwargs):
    if kwargs['update_fields'] is not None and 'status' in kwargs['update_fields']:
        instance.client.potential = False
        instance.client.save(update_fields=['potential'])
