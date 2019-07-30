from rest_framework import serializers

from . import models
from decimal import Decimal, getcontext
getcontext().prec = 2


class WeightPoundsField(serializers.Field):
    """
    Weights are serialized from kilograms to pounds.
    """
    def to_representation(self, value):
        return Decimal(value * 2.204)

    def to_internal_value(self, data):
        return Decimal(value / 2.204)

class WeightStonesField(serializers.Field):
    """
    Weights are serialized from kilograms to stones.
    """
    def to_representation(self, value):

        return Decimal(value * 0.157473)

    def to_internal_value(self, data):
        return Decimal(value / 0.157473)


class HeightFeetField(serializers.Field):
    """
    Height is serialized from cms to feet and inches.
    """
    def to_representation(self, value):
        feet = value // 30.48
        inches = int((value % 30.48) / 2.54)
        return f"{feet} ft {inches} in"

    def to_internal_value(self, data):
        feet, _, inches_ = data.split()
        cm = int(feet)*30.48 + int(float(inches))*2.54
        return cm

class UserSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(format="%Y-%m-%d")
    class Meta:
        model = models.User
        fields = ['id', 'first_name', 'last_name', 'email',
                  'is_active', 'is_staff', 'email_verified',
                  'weight_kg', 'height_cm', 'height_unit',
                  'weight_unit', 'date_of_birth', 'image',
                  'gender', 'number', 'invited',
        ]

class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'first_name', 'last_name', 'email',
                  'image', 'gender', 'number'
        ]
