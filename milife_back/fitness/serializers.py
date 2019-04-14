from rest_framework import serializers
from . import models

class ProgrammeSerializer(serializers.ModelSerializer):
    sessions = serializers.JSONField()

    class Meta:
        model = models.Programme
        fields = '__all__'

class WeightSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return models.Weight.objects.create(
            user = self.context['request'].user,
            **validated_data
        )
    class Meta:
        model = models.Weight
        exclude = ('user',)

class TargetWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TargetWeight
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = '__all__'

class MealPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MealPlan
        fields = '__all__'

# class SessionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=models.Session
#         exclude = ('programme', )

class CheckinSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return models.Checkin.objects.create(
            user = self.context['user'],
            **validated_data,

        )

    class Meta:
        model = models.Checkin
        exclude = ('accuniq_timestamp', 'accuniq_data', 'user')


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Holiday
        fields = '__all__'


class SessionLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SessionLedger
        fields = '__all__'


