# Generated by Django 2.1 on 2018-08-09 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ambition_prn', '0005_auto_20180708_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deathreport',
            name='tracking_identifier',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='deathreporttmg',
            name='tracking_identifier',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='historicaldeathreport',
            name='tracking_identifier',
            field=models.CharField(db_index=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='historicaldeathreporttmg',
            name='tracking_identifier',
            field=models.CharField(db_index=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='historicalprotocoldeviationviolation',
            name='tracking_identifier',
            field=models.CharField(db_index=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='historicalstudyterminationconclusion',
            name='tracking_identifier',
            field=models.CharField(db_index=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='historicalstudyterminationconclusionw10',
            name='tracking_identifier',
            field=models.CharField(db_index=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='protocoldeviationviolation',
            name='tracking_identifier',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='studyterminationconclusion',
            name='tracking_identifier',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='studyterminationconclusionw10',
            name='tracking_identifier',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
