from rest_framework import serializers
from . import models

class ProgrammeSerializer(serializers.ModelSerializer):
    sessions = serializers.JSONField(required=False)

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
        exclude = ('user', 'created_at', 'modified_at')

class TargetWeightSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return models.TargetWeight.objects.create(
            user = self.context['user_ref'],
            **validated_data
        )

    class Meta:
        model = models.TargetWeight
        exclude = ('user', 'created_at', 'modified_at')


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
    def create(self, validated_data):
        return models.MealPlan.objects.create(
            user = self.context['user_ref'],
            **validated_data,
        )

    class Meta:
        model = models.MealPlan
        exclude = ('user', )


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


class ProgressReportSerializer(serializers.ModelSerializer):
    """
    body_fat: {mbf_quantity, mbf_low_limit, mbf_standard, mbf_top_limit}
    percentage_body_fat: {pbf_rate, pbf_min_limit, pbf_low_limit, pbf_top_limit, pbf_topmax_limit, pbf_max_limit},
    muscle_mass: {muscle_quantity, muscle_low_limit, muscle_standard , muscle_top_limit}
    """
    class Meta:
        model = models.Checkin
        fields = '__all__'


class ProgressReportSummarySerializer(serializers.ModelSerializer):
    body_fat = serializers.SerializerMethodField()
    muscle_mass = serializers.SerializerMethodField()

    class Meta:
        model = models.Checkin
        fields = ('body_fat', 'muscle_mass', 'date_of_checkin',  )

    def get_body_fat(self, obj):
        return obj.accuniq_data['mbf_quantity']

    def get_muscle_mass(self, obj):
        return obj.accuniq_data['muscle_quantity']


class ClientDashboardSerializer(serializers.Serializer):
    weight_log = WeightSerializer(many=True)
    target_weight = TargetWeightSerializer(many=True)
    calorie = serializers.IntegerField()
    # progress_report = ProgressReportSerializer(many=True)
    messages_count = serializers.IntegerField()
    progress_report = ProgressReportSummarySerializer(many=True)
