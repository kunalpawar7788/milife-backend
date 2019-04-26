# Generated by Django 2.1.2 on 2019-04-23 11:52

import django.contrib.postgres.fields.hstore
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0017_message_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mealplan',
            name='carbohydrate',
        ),
        migrations.RemoveField(
            model_name='mealplan',
            name='fat',
        ),
        migrations.RemoveField(
            model_name='mealplan',
            name='name',
        ),
        migrations.RemoveField(
            model_name='mealplan',
            name='protein',
        ),
        migrations.AddField(
            model_name='mealplan',
            name='calorie',
            field=models.IntegerField(default=0, verbose_name='Calorie'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='daily_percentages',
            field=django.contrib.postgres.fields.hstore.HStoreField(default=dict),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='meal_percentage',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='message',
            name='kind',
            field=models.CharField(choices=[('weekly-commentry', 'Weekly Commentry'), ('misc', 'MISCELLANEOUS')], max_length=120, verbose_name='Message type'),
        ),
    ]
