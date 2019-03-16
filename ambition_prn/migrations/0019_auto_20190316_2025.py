# Generated by Django 2.1.7 on 2019-03-16 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ambition_prn', '0018_auto_20190305_0123'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalstudyterminationconclusion',
            name='on_study_drug',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes', max_length=25, verbose_name="Has the patient started 'study' drug"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studyterminationconclusion',
            name='on_study_drug',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes', max_length=25, verbose_name="Has the patient started 'study' drug"),
            preserve_default=False,
        ),
    ]
