from django.dispatch import receiver
from django.db.models.signals import post_save

from contracts import models as contracts_models


@receiver(post_save, sender=contracts_models.Contract)
def update_client_from_potential_to_existant(sender, instance,
                                             *args, **kwargs):
    if kwargs['update_fields'] is not None \
            and 'status' in kwargs['update_fields']:
        instance.client.potential = False
        instance.client.save(update_fields=['potential'])
