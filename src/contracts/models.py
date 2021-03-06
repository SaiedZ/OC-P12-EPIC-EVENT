from django.db import models
from teams.models import CRMUser

from clients.models import Client


class Contract(models.Model):
    """Contract model."""

    sales_contact = models.ForeignKey(
        to=CRMUser,
        related_name="sales_contact",
        on_delete=models.PROTECT,
        help_text="Must be part of the sale team.",
    )
    client = models.ForeignKey(
        to=Client,
        related_name="client",
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    amount = models.FloatField()
    payment_due = models.DateTimeField()

    def __str__(self):
        return f"{self.client} - " f"{self.sales_contact}"
