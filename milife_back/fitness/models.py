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


# class Session(TimeStampedUUIDModel):
#     """
#     A programme shall have many sessions.
#     """
#     programme = models.ForeignKey(
#         Programme,
#         on_delete=models.CASCADE,
#         related_name="programme_schedule")
#     weekday = models.CharField(_("Weekday"), max_length=20)
#     start_time = models.TimeField()
#     deleted = models.BooleanField(_('Deleted'), default=False)


class Schedule(TimeStampedUUIDModel):
    """
    A programme shall have many sessions.
    """
    STATUS_CHOICES = (
        ("scheduled", 'scheduled'),
        ('availed', 'availed'),
        ('cancelled', 'cancelled'),
        ('banked', 'banked'),
    )
    programme = models.ForeignKey(
        Programme,
        on_delete=models.CASCADE,
        related_name="programme_schedule")
    coach = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="sechudle_coach")

    start = models.DateTimeField()
    end = models.DateTimeField()
    name = models.CharField(_("Session name"), max_length=120)
    status = models.CharField(_("State of the session"), max_length=20)


class Holiday(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="schedule_user")
    start = models.DateField()
    end = models.DateField()


class Weight(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="weight_user")
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
    accuniq_data = HStoreField()


class MealPlan(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="mealplan_user")
    name = models.CharField(_("Name of Meal"), max_length=120)
    carbohydrate = models.IntegerField(_("Carbohydrate"))
    fat = models.IntegerField(_("Fat"))
    protein = models.IntegerField(_("Protein"))


