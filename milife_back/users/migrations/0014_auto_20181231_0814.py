# Generated by Django 2.1.2 on 2018-12-31 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20181229_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='accuniq_id',
            field=models.CharField(default='blah', max_length=100, verbose_name='Accuniq Id'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='height_unit',
            field=models.CharField(blank=True, choices=[('ft', 'feet and inches'), ('cm', 'centimeters')], max_length=4, verbose_name='Height unit preference'),
        ),
        migrations.AlterField(
            model_name='user',
            name='weight_unit',
            field=models.CharField(blank=True, choices=[('kg', 'kilogram'), ('st', 'stones'), ('lb', 'pounds')], max_length=4, verbose_name='Weight unit preference'),
        ),
    ]
