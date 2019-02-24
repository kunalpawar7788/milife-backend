# Generated by Django 2.1.2 on 2019-02-24 10:43

import django.contrib.postgres.fields.hstore
from django.db import migrations, models
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0008_auto_20190224_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='accuniq_data',
            field=django.contrib.postgres.fields.hstore.HStoreField(default=dict),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='accuniq_timestamp',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='photo_front_profile',
            field=versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='checkin_images', verbose_name='front_profile'),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='photo_side_profile',
            field=versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='checkin_images', verbose_name='side_profile'),
        ),
    ]
