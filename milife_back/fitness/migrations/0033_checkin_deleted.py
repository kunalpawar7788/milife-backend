# Generated by Django 2.1.2 on 2020-01-30 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0032_auto_20191028_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkin',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Deleted'),
        ),
    ]
