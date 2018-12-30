from rest_framework import serializers
from drf_extra_fields.fields import DateTimeRangeField

from . import models

class ScheduleSerializer(serializers.ModelSerializer):
    session = DateTimeRangeField()
    class Meta:
        model = models.Schedule
        fields = '__all__'

