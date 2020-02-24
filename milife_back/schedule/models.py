from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from milife_back.base.models import TimeStampedUUIDModel
from psycopg2.extras import DateTimeTZRange

class Schedule(TimeStampedUUIDModel):
    trainee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="schedule_trainee")
    trainer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="schedule_trainer")
    start = models.DateTimeField(_("Start time of the session"))
    end = models.DateTimeField(_("End time of the session"))
    session = DateTimeTZRange()
    deleted = models.BooleanField(_('Deleted'), default=False)


