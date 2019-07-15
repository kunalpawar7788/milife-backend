from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from . import models
from . import services

from milife_back.users.models import User

@receiver(post_save, sender=models.AccuniqData)
def create_accuniqdata_callback(sender, instance, created, **kwargs):
    services.populate_checkin_from_accuniq_data(instance.id)

@receiver(pre_save, sender=models.Checkin)
def create_message_for_checkin(sender, instance, raw, using, update_fields, **kwargs1):
    if instance.comment:
        return
    message = models.Message.objects.create(
        recipient = instance.user,
        sender = User.objects.all()[0],
        kind = "checkin-commentry",
        content = "",
        deleted=True,
    )
    instance.comment = message
