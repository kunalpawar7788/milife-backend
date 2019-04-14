from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from milife_back.base.models import TimeStampedUUIDModel
from versatileimagefield.fields import VersatileImageField

from django.contrib.postgres.fields import HStoreField

class Programme(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="programme_user")
    coach = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="programme_coach")
    name = models.CharField(_("Programme Name"), max_length=120)
    start_date = models.DateField()
    end_date = models.DateField()
    sessions = HStoreField(default=dict)
    active = models.BooleanField(_('Active'), default=True)


class Holiday(TimeStampedUUIDModel):
    EFFECT_ON_SCHEDULE_CHOICES = (
        ('extend_programme', 'Extend Programme'),
        ('bank_sessions', 'Bank Sessions'),
    )
    programme = models.ForeignKey(Programme, on_delete=models.PROTECT, related_name='holiday_programme')
    start = models.DateField()
    end = models.DateField()
    comment= models.CharField(_("Comment"), max_length=200, blank=True)


class SessionLedger(TimeStampedUUIDModel):
    TYPES = (
        ('C', 'CREDITED'),
        ('D', 'DEBITED')
    )
    programme = models.ForeignKey(Programme, on_delete=models.PROTECT, related_name='sessionledger_programme')
    start = models.DateTimeField()
    comment = models.CharField(_("Comment"), max_length=200, blank=True)
    kind = models.CharField(_("credit/debit"), max_length=4, choices=TYPES)


class TargetWeight(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="weight_user")
    target_weight = models.FloatField(_("Weight"))


class Weight(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="target_weight_user")
    weight = models.FloatField(_("Weight"))
    measured_on = models.DateField(_("Measured on"))


class Message(TimeStampedUUIDModel):
    MESSAGE_TYPES=[('weekly_commentry', 'Weekly Commentry'), ]
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="message_recipient")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="message_sender")
    kind = models.CharField(_("Message type"), max_length=120, choices=MESSAGE_TYPES)
    read = models.BooleanField(_('Has been read by the recipient'), default=False)
    deleted = models.BooleanField(_('Deleted'), default=False)


class Checkin(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="checkin_user")
    date_of_checkin = models.DateField()
    accuniq_timestamp = models.DateTimeField(null=True)
    accuniq_data = HStoreField(default=dict)

    photo_front_profile = VersatileImageField("front_profile", upload_to="checkin_images", blank=True, null=True)
    photo_side_profile = VersatileImageField("side_profile", upload_to="checkin_images", blank=True, null=True)

    waist = models.DecimalField(_("waist"), max_digits=5, decimal_places=2, default=0)
    hips = models.DecimalField(_("hips"), max_digits=5, decimal_places=2, default=0)
    chest = models.DecimalField(_("chest"), max_digits=5, decimal_places=2, default=0)
    shoulders = models.DecimalField(_("shoulders"), max_digits=5, decimal_places=2, default=0)
    left_arm = models.DecimalField(_("left_arm"), max_digits=5, decimal_places=2, default=0)
    right_arm = models.DecimalField(_("right_arm"), max_digits=5, decimal_places=2, default=0)
    left_leg = models.DecimalField(_("left_leg"), max_digits=5, decimal_places=2, default=0)
    right_leg = models.DecimalField(_("right_leg"), max_digits=5, decimal_places=2, default=0)

    class Meta:
        unique_together=(('user', 'date_of_checkin'),)


class MealPlan(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="mealplan_user")
    name = models.CharField(_("Name of Meal"), max_length=120)
    carbohydrate = models.IntegerField(_("Carbohydrate"))
    fat = models.IntegerField(_("Fat"))
    protein = models.IntegerField(_("Protein"))


