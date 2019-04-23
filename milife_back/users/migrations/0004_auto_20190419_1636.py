# Generated by Django 2.1.2 on 2019-04-19 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile_picture',
        ),
        migrations.AlterField(
            model_name='user',
            name='weight_unit',
            field=models.CharField(blank=True, choices=[('metric', 'metric'), ('imperial', 'imperial')], max_length=10, verbose_name='Weight unit preference'),
        ),
    ]
