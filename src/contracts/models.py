from django.db import models
from teams.models import CRMUser

from clients import models as clients_models

class Contract(models.Model):
    """Contract model."""

    sales_contact = models.ForeignKey(
        to=CRMUser,
        related_name='sales_contact',
        on_delete=models.PROTECT,
    )
    client = models.ForeignKey(
        to=clients_models.Client,
        related_name='client',
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    amount = models.FloatField()
    payment_due = models.DateTimeField()
