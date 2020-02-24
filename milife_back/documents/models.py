from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from milife_back.base.models import TimeStampedUUIDModel

class Document(TimeStampedUUIDModel):
    TYPE_CHOICES = (
        ('MEALPLAN', 'MEAL PLAN'),
        ('CLIENTAGREEMENT', 'CLIENT AGREEMENT'),
        ('PARQ', 'PARQ'),
        ('GUARANTEE', 'GUARANTEE'),
        ('MISC', 'MISC')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="trainee")
    document = models.FileField(_('Document'))
    name = models.CharField(_("Document's Name"), max_length=120, blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="trainer")
    deleted = models.BooleanField(_('Deleted'), default=False)
    notes = models.TextField(_('Notes'), max_length=2000, blank=True)
    kind = models.CharField(_('type'), max_length=50, blank=True, choices=TYPE_CHOICES)
