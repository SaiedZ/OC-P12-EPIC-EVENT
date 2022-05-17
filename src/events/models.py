from django.db import models
from django.utils.translation import gettext_lazy as _

from teams.models import CRMUser
from contracts.models import Contract
from .managers import UniqueNameManager


class Event(models.Model):
    """Event model."""

    contract = models.OneToOneField(
        to=Contract,
        on_delete=models.CASCADE,
        related_name="contract",
    )
    support_contact = models.ForeignKey(
        to=CRMUser,
        on_delete=models.PROTECT,
        related_name="support_contact",
    )
    status = models.ForeignKey(
        to='EventStatus',
        on_delete=models.PROTECT,
        related_name="event_statut",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    attendees = models.IntegerField(blank=True, null=True)
    event_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)


class EventStatus(models.Model):
    """Represents the Team of the user."""

    name = models.CharField(_("Event statut"), max_length=200, unique=True)

    objects = UniqueNameManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def natural_key(self):
        """Returns the natural key used for fixture serialization."""
        return self.name
