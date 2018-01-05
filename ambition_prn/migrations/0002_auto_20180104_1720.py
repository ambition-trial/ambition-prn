# Generated by Django 2.0 on 2018-01-04 15:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ambition_prn', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deathreport',
            name='study_day',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Study day'),
        ),
        migrations.AlterField(
            model_name='historicaldeathreport',
            name='study_day',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Study day'),
        ),
    ]