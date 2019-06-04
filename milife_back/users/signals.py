from django.db.models.signals import pre_save
from django.dispatch import receiver

from . import models
from . import services


@receiver(pre_save, sender=models.User)
def create_accuniq_id(sender, instance, **kwargs):
    instance.accuniq_id = services.create_accuniq_id(instance.first_name, instance.last_name)
