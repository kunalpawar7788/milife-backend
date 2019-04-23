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
            user = self.context['user_ref'],
            **validated_data
        )
    class Meta:
        model = models.Weight
        exclude = ('user',)

class TargetWeightSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return models.TargetWeight.objects.create(
            user = self.context['user_ref'],
            **validated_data
        )

    class Meta:
        model = models.TargetWeight
        exclude = ('user',)


class MessageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return models.Message.objects.create(
            sender = self.context['sender'],
            recipient = self.context['recipient'],
            **validated_data
        )

    class Meta:
        model = models.Message
        fields = ('kind', 'content', 'read', 'deleted')

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


