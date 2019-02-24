from rest_framework import serializers
from . import models

class ProgrammeSerializer(serializers.ModelSerializer):
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
