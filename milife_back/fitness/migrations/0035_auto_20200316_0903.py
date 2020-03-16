# Generated by Django 2.1.2 on 2020-03-16 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0034_auto_20200224_0846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='blood_sugar',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5, verbose_name='blood_sugar'),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='chest',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5, verbose_name='chest'),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='diastolic_blood_pressure',
            field=models.IntegerField(default=0, verbose_name='diastolic_blood_pressure'),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='hips',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5, verbose_name='hips'),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='left_arm',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5, verbose_name='left_arm'),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='left_leg',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5, verbose_name='left_leg'),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='right_arm',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5, verbose_name='right_arm'),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='right_leg',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5, verbose_name='right_leg'),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='shoulders',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5, verbose_name='shoulders'),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='systolic_blood_pressure',
            field=models.IntegerField(default=0, verbose_name='systolic_blood_pressure'),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='vo2_max',
            field=models.IntegerField(default=0, verbose_name='vo2_max'),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='waist',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5, verbose_name='waist'),
        ),
    ]
