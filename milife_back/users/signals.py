from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from . import models
from . import services

from milife_back.fitness.models import Checkin

@receiver(pre_save, sender=models.User)
def create_accuniq_id(sender, instance, **kwargs):
    instance.accuniq_id = services.create_accuniq_id(instance.first_name, instance.last_name)

@receiver(post_save, sender=models.User)
def update_checkin_objects(sender, instance, created, **kwargs):
    Checkin.objects.filter(user=None, accuniq_id=instance.accuniq_id).update(user=instance)
