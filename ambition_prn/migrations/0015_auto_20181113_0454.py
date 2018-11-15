# Generated by Django 2.1.2 on 2018-11-13 02:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ambition_prn', '0014_auto_20181112_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalstudyterminationconclusion',
            name='blood_received',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='unk', max_length=25, verbose_name='Blood transfusion received?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalstudyterminationconclusion',
            name='units',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='If YES, no. of units'),
        ),
        migrations.AddField(
            model_name='studyterminationconclusion',
            name='blood_received',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='unk', max_length=25, verbose_name='Blood transfusion received?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studyterminationconclusion',
            name='units',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='If YES, no. of units'),
        ),
    ]
