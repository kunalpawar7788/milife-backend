from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models
from . import services


@receiver(post_save, sender=models.AccuniqData)
def create_accuniqdata_callback(sender, instance, created, **kwargs):
    services.populate_checkin_from_accuniq_data(instance.id)
