from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from milife_back.base.models import TimeStampedUUIDModel
from versatileimagefield.fields import VersatileImageField

from django.contrib.postgres.fields import HStoreField
from django.contrib.postgres.fields import JSONField

from django.utils import timezone

class Programme(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="programme_user")
    coach = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="programme_coach")
    name = models.CharField(_("Programme Name"), max_length=120)
    start_date = models.DateField()
    end_date = models.DateField()
    sessions = HStoreField(default=dict)
    active = models.BooleanField(_('Active'), default=True)



class Holiday(TimeStampedUUIDModel):
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='holiday2programme')
    start = models.DateField()
    end = models.DateField()
    comment= models.CharField(_("Comment"), max_length=200, blank=True)
    programme_end_date = models.DateField()


class LeaveLedger(TimeStampedUUIDModel):
    TYPES = (
        ('C', 'CREDITED'),
        ('D', 'DEBITED')
    )

    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='leaveledger2programme')
    date = models.DateField()
    kind = models.CharField(_("credit/debit"), max_length=4, choices=TYPES)


class TargetWeight(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="weight_user")
    target_date = models.DateField(_("end_date"), default=timezone.now)
    target_weight = models.FloatField(_("Target Weight"), default=0)


class Weight(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="target_weight_user")
    weight = models.FloatField(_("Weight"), default=0)
    measured_on = models.DateField(_("Measured on"), default=timezone.now)


class Message(TimeStampedUUIDModel):
    MESSAGE_TYPES=[
        ('checkin-commentry', 'Checkin Commentry'),
        ('weekly-commentry', 'Weekly Commentry'),
        ('misc', 'MISCELLANEOUS')
    ]
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="message_recipient")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="message_sender")
    kind = models.CharField(_("Message type"), max_length=120, choices=MESSAGE_TYPES)
    read = models.BooleanField(_('Has been read by the recipient'), default=False)
    deleted = models.BooleanField(_('Deleted'), default=False)
    content = models.TextField(_("Content"), blank=True)


class Checkin(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="checkin_user", blank=True, null=True)
    accuniq_id = models.CharField(_("Accuniq Id"), max_length=21, default="")

    # use date_of_checkin for all calculation.
    date_of_checkin = models.DateField(_("Date of checkin"), blank=True, null=True)

    # this timestapm is only used to refrain from upserting existing values.
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

    systolic_blood_pressure = models.IntegerField(_("systolic_blood_pressure"), default=0)
    diastolic_blood_pressure = models.IntegerField(_("diastolic_blood_pressure"), default=0)
    blood_sugar = models.DecimalField(_("blood_sugar"), max_digits=5, decimal_places=1, default=0)
    vo2_max = models.IntegerField(_("vo2_max"), default=0)
    resting_heart_rate = models.IntegerField(_("resting heart rate"), default=0)
    comment = models.OneToOneField(Message, on_delete=models.CASCADE, related_name="comment_of", null=True)
    deleted = models.BooleanField(_('Deleted'), default=False)

    class Meta:
        unique_together=(('accuniq_id', 'accuniq_timestamp'),)


class MealPlan(TimeStampedUUIDModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mealplan_user")
    calorie = models.IntegerField(_("Calorie"), default=0)
    daily_breakup = JSONField(default=dict)
    meal_breakup = JSONField(default=list)


class AccuniqData(TimeStampedUUIDModel):
    csvfile = models.FileField(_("accuniq csvfile"), upload_to="accuniq")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="accuniqdata_user")
