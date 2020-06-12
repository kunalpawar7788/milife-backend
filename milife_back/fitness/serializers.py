from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin

from . import models
from ..users.serializers import CoachSerializer
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


class BulkWeightSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    def create(self, validated_data):
        weight, created = models.Weight.objects.get_or_create(
            user=validated_data['user'],
            measured_on=validated_data['measured_on'],
        )

        weight.weight = validated_data['weight']
        weight.save()

        return weight

    class Meta:
        model=models.Weight
        list_serializer_class = BulkListSerializer
        fields = ('user', 'weight', 'measured_on')


class BulkTargetWeightSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    def create(self, validated_data):
        t_weight, created = models.TargetWeight.objects.get_or_create(
            user=validated_data['user'],
            target_date=validated_data['target_date'],
        )

        t_weight.target_weight = validated_data['target_weight']
        t_weight.save()

        return t_weight

    class Meta:
        model=models.TargetWeight
        list_serializer_class = BulkListSerializer
        fields = ('user', 'target_weight', 'target_date')


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
    sender = CoachSerializer(read_only=True)

    def create(self, validated_data):
        return models.Message.objects.create(
            sender = self.context['sender'],
            recipient = self.context['recipient'],
            **validated_data
        )

    def update(self, instance, validated_data):
        print(self.context['sender'], instance.sender)
        if self.context['sender'].is_staff:
            instance.sender = self.context['sender']
            # instance.save()
        return super(MessageSerializer, self).update(instance, validated_data)

    class Meta:
        model = models.Message
        fields = ('kind', 'content', 'read', 'deleted', 'created_at', 'modified_at', 'id', 'sender')
        read_only_fields = ('created_at', 'modified_at', 'id')

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
        exclude = ( 'programme', )

    def create(self, validated_data):
        return models.Holiday.objects.create(
            programme = self.context['programme'],
            **validated_data,
        )

class LeaveLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LeaveLedger
        exclude = ( 'programme', )

    def create(self, validated_data):
        return models.LeaveLedger.objects.create(
            programme = self.context['programme'],
            **validated_data,
        )


class ProgressReportSerializer(serializers.ModelSerializer):
    """
    body_fat: {mbf_quantity, mbf_low_limit, mbf_standard, mbf_top_limit}
    percentage_body_fat: {pbf_rate, pbf_min_limit, pbf_low_limit, pbf_top_limit, pbf_topmax_limit, pbf_max_limit},
    muscle_mass: {muscle_quantity, muscle_low_limit, muscle_standard , muscle_top_limit}
    """
    comment = MessageSerializer(read_only=True)

    class Meta:
        model = models.Checkin
        fields = '__all__'


class ProgressReportSummarySerializer(serializers.ModelSerializer):
    body_fat = serializers.SerializerMethodField()
    percentage_body_fat = serializers.SerializerMethodField()
    percentage_muscle_mass = serializers.SerializerMethodField()
    muscle_mass = serializers.SerializerMethodField()
    month = serializers.SerializerMethodField()

    class Meta:
        model = models.Checkin
        fields = ('body_fat',
                  'muscle_mass',
                  'date_of_checkin',
                  'percentage_body_fat',
                  'percentage_muscle_mass',
                  'month',
        )

    def _percentage(self, n, d):
        return round(100*(float(n)/float(d)), 1)

    def get_body_fat(self, obj):
        return float(obj.accuniq_data.get('mbf_quantity',0))/10

    def get_muscle_mass(self, obj):
        return float(obj.accuniq_data.get('muscle_quantity',0))/10

    def get_percentage_body_fat(self, obj):
        if not obj.accuniq_data:
            return 0
        return self._percentage(obj.accuniq_data['mbf_quantity'], obj.accuniq_data['weight'])

    def get_percentage_muscle_mass(self, obj):
        if not obj.accuniq_data:
            return 0
        return self._percentage(obj.accuniq_data['muscle_quantity'], obj.accuniq_data['weight'])

    def get_month(self, obj):
        return obj.date_of_checkin.strftime("%b %y")


class ClientDashboardSerializer(serializers.Serializer):
    weight_log = WeightSerializer(many=True)
    target_weight = TargetWeightSerializer(many=True)
    calorie = serializers.IntegerField()
    # progress_report = ProgressReportSerializer(many=True)
    messages_count = serializers.IntegerField()
    progress_report = ProgressReportSummarySerializer(many=True)
    programme = ProgrammeSerializer()
    first_checkin = CheckinSerializer()


class ProgressReportDetailSerializer(serializers.ModelSerializer):
    body_fat = serializers.SerializerMethodField()
    percentage_body_fat = serializers.SerializerMethodField()
    percentage_muscle_mass = serializers.SerializerMethodField()
    muscle_mass = serializers.SerializerMethodField()
    visceral_fat_mass  = serializers.SerializerMethodField()
    body_type = serializers.SerializerMethodField()
    biological_age = serializers.SerializerMethodField()
    body_mass_index = serializers.SerializerMethodField()
    waist_hip_ratio = serializers.SerializerMethodField()

    month = serializers.SerializerMethodField()
    comment = MessageSerializer(read_only=True)

    class Meta:
        model = models.Checkin
        fields = ('body_fat',
                  'muscle_mass',
                  'date_of_checkin',
                  'percentage_body_fat',
                  'percentage_muscle_mass',
                  'month',
                  'visceral_fat_mass',
                  'body_type',
                  'biological_age',
                  'body_mass_index',
                  'waist_hip_ratio',


                  'systolic_blood_pressure',
                  'diastolic_blood_pressure',
                  'blood_sugar',
                  'vo2_max',
                  'resting_heart_rate',
                  'waist',
                  'hips',
                  'chest',
                  'shoulders',
                  'left_arm',
                  'right_arm',
                  'left_leg',
                  'right_leg',
                  'photo_front_profile',
                  'photo_side_profile',

                  'comment',
        )

    def _percentage(self, n, d):
        return round(100*(float(n)/float(d)), 1)

    def get_body_fat(self, obj):
        if 'FM' in obj.accuniq_data:
           return float(obj.accuniq_data.get('FM',0))/10
        return float(obj.accuniq_data.get('mbf_quantity',0))/10

    def get_visceral_fat_mass(self, obj):
        if 'mvf_quantity' in obj.accuniq_data:
            return float(obj.accuniq_data.get('mvf_quantity',0))/10
        return float(obj.accuniq_data.get('VFM',0))/10

    def get_body_type(self, obj):
        if 'Body_Type' in obj.accuniq_data:
           return int(obj.accuniq_data.get('Body_Type',0))
        return int(obj.accuniq_data.get('fat_type',0))

    def get_biological_age(self, obj):
        if 'Body_Age' in obj.accuniq_data:
           return int(obj.accuniq_data.get('Body_Age', 0))
        return int(obj.accuniq_data.get('body_age', 0))

    def get_body_mass_index(self, obj):
        if 'BMI' in obj.accuniq_data:
           return int(obj.accuniq_data.get('BMI',0))
        return float(obj.accuniq_data.get('bmi',0))/10

    def get_waist_hip_ratio(self, obj):
        if 'WHR' in obj.accuniq_data:
           return float(obj.accuniq_data.get('WHR', 0))/100
        return float(obj.accuniq_data.get('whr_rate', 0))/100

    def get_muscle_mass(self, obj):
        if 'Skeletal_Muscle' in obj.accuniq_data:
           return float(obj.accuniq_data.get('Skeletal_Muscle',0))/10
        return float(obj.accuniq_data.get('bone_slim',0))/10

    def get_percentage_body_fat(self, obj):
        if not obj.accuniq_data:
            return 0
        if 'FM' in obj.accuniq_data:
           return self._percentage(obj.accuniq_data['FM'], obj.accuniq_data['Weight'])
        return self._percentage(obj.accuniq_data['mbf_quantity'], obj.accuniq_data['weight'])

    def get_percentage_muscle_mass(self, obj):
        if not obj.accuniq_data:
            return 0
        if 'Skeletal_Muscle' in obj.accuniq_data:
           return self._percentage(obj.accuniq_data['Skeletal_Muscle'], obj.accuniq_data['Weight'])
        return self._percentage(obj.accuniq_data['bone_slim'], obj.accuniq_data['weight'])

    def get_month(self, obj):
        return obj.date_of_checkin.strftime("%b %y")


class  AccuniqDataSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return models.AccuniqData.objects.create(
            uploaded_by = self.context['uploaded_by'],
            **validated_data,
        )

    class Meta:
        model = models.AccuniqData
        exclude = ('uploaded_by',)


class WeightChartSerializer(serializers.Serializer):
    weight_log = WeightSerializer(many=True)
    target_weight = TargetWeightSerializer(many=True)
