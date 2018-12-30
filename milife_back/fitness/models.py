from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from milife_back.base.models import TimeStampedUUIDModel
from versatileimagefield.fields import VersatileImageField

class Programme(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="weight_user")
    coach = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="weight_coach")
    name = models.CharField(_("Programme Name"), max_length=120)
    start_date = models.DateField()
    end_date = models.DateField()


class Weight(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="weight_user")
    weight = models.FloatField(_("Weight"))
    measured_on = models.DateField(_("Measured on"))


class Message(TimeStampedUUIDModel):
    MESSAGE_TYPES=['Weekly Commentry', '']

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="message_recipient")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="message_sender")
    kind = models.ChoiceField(_("Message type"), choices=MESSAGE_TYPES)
    read = models.BooleanField(_('Has been read by the recipient'), default=False)


class Checkin(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="weight_user")
    body_water = models.FloatField(_("Body Water"))
    proteins = model.FloatField(_("Proteins"))
    minerals = models.FloatField(_("Minerals"))
    body_fat = models.FloatField(_("Body fat"))
    body_fat_percentage = models.FloatField(_("Body fat percentage"))
    muscle_mass = models.FloatField(_("Muscle Mass"))
    muscle_mass_percentage = models.FloatField(_("muscle mass percentage"))
    visceral_fat_mass = models.FloatField(_("visteral fat mass"))
    body_type=models.FloatField(_("Body Type"))
    biological_age = models.IntegerField(_("Biological Age"))
    waist = models.FloatField(_("Waist"))
    hips = models.FloatField(_("Hips"))
    chest = models.FloatField(_("Chest"))
    shoulders = models.FloatField(_("Shoulders"))
    left_arm = models.FloatField(_("Left Arm"))
    right_arm = models.FloatField(_("Right Arm"))
    left_leg = models.FloatField(_("Left Leg"))
    right_leg = models.FloatField(_("Right Leg"))
    waist = models.FloatField(_("Waist"))
    waist = models.FloatField(_("Waist"))
    waist = models.FloatField(_("Waist"))
    lean_mass_trunk = models.FloatField(_("lean_mass_trunk"))
    lean_mass_left_arm = models.FloatField(_("Lean Mass Left Arm"))
    lean_mass_right_arm = models.FloatField(_("Lean Mass Right Arm"))
    lean_mass_left_leg = models.FloatField(_("Lean Mass Left Leg"))
    lean_mass_right_leg = models.FloatField(_("Lean Mass Right Leg"))

    # bmi to be calculated

    # waist_hip_ratio calculated

    systolic_blood_pressure = models.FloatField(_("Systolic Blood Pressure"))
    diastolic_blood_pressure = models.FloatField(_("Diatolic Blood Pressure"))
    blood_sugar = models.FloatField(_("Blood Sugar"))
    vo2max = models.FloatField(_("VO2Max"))
    resting_heart_rate = models.FloatField(_("Resting Heart Rate"))
    photo_front = VersatileImageField(_("Front Photo"), upload_to="checkin_images/")
    photo_side = VersatileImageField(_("Side Photo"), upload_to="checkin_images/")
    # Body Type chart


class MealPlan(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="weight_user")
    name = models.CharField(_("Name of Meal"), max_length=120)
    carbohydrate = models.IntegerField(_("Carbohydrate"), min_value=0, max_value=100)
    fat = models.IntegerField(_("Fat"), min_value=0, max_value=100)
    protein = models.IntegerField(_("Protein"), min_value=0, max_value=100)


