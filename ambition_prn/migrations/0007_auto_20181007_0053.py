# Generated by Django 2.1 on 2018-10-06 22:53

from django.db import migrations, models
import django.db.models.deletion
import edc_action_item.managers
import edc_identifier.managers
import edc_visit_schedule.model_mixins.schedule_model_mixin


class Migration(migrations.Migration):

    dependencies = [
        ('edc_action_item', '0011_auto_20181009_2236'),
        ('ambition_prn', '0006_auto_20180809_0504'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='deathreport',
            managers=[
                ('on_site', edc_action_item.managers.ActionIdentifierSiteManager()),
                ('objects', edc_action_item.managers.ActionIdentifierManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='deathreporttmg',
            managers=[
                ('on_site', edc_action_item.managers.ActionIdentifierSiteManager()),
                ('objects', edc_action_item.managers.ActionIdentifierManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='onschedule',
            managers=[
                ('on_site', edc_visit_schedule.model_mixins.schedule_model_mixin.CurrentSiteManager()),
                ('objects', edc_identifier.managers.SubjectIdentifierManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='onschedulew10',
            managers=[
                ('on_site', edc_visit_schedule.model_mixins.schedule_model_mixin.CurrentSiteManager()),
                ('objects', edc_identifier.managers.SubjectIdentifierManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='protocoldeviationviolation',
            managers=[
                ('on_site', edc_action_item.managers.ActionIdentifierSiteManager()),
                ('objects', edc_action_item.managers.ActionIdentifierManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='studyterminationconclusion',
            managers=[
                ('on_site', edc_action_item.managers.ActionIdentifierSiteManager()),
                ('objects', edc_action_item.managers.ActionIdentifierManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='studyterminationconclusionw10',
            managers=[
                ('on_site', edc_action_item.managers.ActionIdentifierSiteManager()),
                ('objects', edc_action_item.managers.ActionIdentifierManager()),
            ],
        ),
        migrations.RenameField(
            model_name='deathreport',
            old_name='parent_reference_identifier',
            new_name='parent_action_identifier',
        ),
        migrations.RenameField(
            model_name='deathreport',
            old_name='related_reference_identifier',
            new_name='related_action_identifier',
        ),
        migrations.RenameField(
            model_name='deathreporttmg',
            old_name='parent_reference_identifier',
            new_name='parent_action_identifier',
        ),
        migrations.RenameField(
            model_name='deathreporttmg',
            old_name='related_reference_identifier',
            new_name='related_action_identifier',
        ),
        migrations.RenameField(
            model_name='historicaldeathreport',
            old_name='parent_reference_identifier',
            new_name='parent_action_identifier',
        ),
        migrations.RenameField(
            model_name='historicaldeathreport',
            old_name='related_reference_identifier',
            new_name='related_action_identifier',
        ),
        migrations.RenameField(
            model_name='historicaldeathreporttmg',
            old_name='parent_reference_identifier',
            new_name='parent_action_identifier',
        ),
        migrations.RenameField(
            model_name='historicaldeathreporttmg',
            old_name='related_reference_identifier',
            new_name='related_action_identifier',
        ),
        migrations.RenameField(
            model_name='historicalprotocoldeviationviolation',
            old_name='parent_reference_identifier',
            new_name='parent_action_identifier',
        ),
        migrations.RenameField(
            model_name='historicalprotocoldeviationviolation',
            old_name='related_reference_identifier',
            new_name='related_action_identifier',
        ),
        migrations.RenameField(
            model_name='historicalstudyterminationconclusion',
            old_name='parent_reference_identifier',
            new_name='parent_action_identifier',
        ),
        migrations.RenameField(
            model_name='historicalstudyterminationconclusion',
            old_name='related_reference_identifier',
            new_name='related_action_identifier',
        ),
        migrations.RenameField(
            model_name='historicalstudyterminationconclusionw10',
            old_name='parent_reference_identifier',
            new_name='parent_action_identifier',
        ),
        migrations.RenameField(
            model_name='historicalstudyterminationconclusionw10',
            old_name='related_reference_identifier',
            new_name='related_action_identifier',
        ),
        migrations.RenameField(
            model_name='protocoldeviationviolation',
            old_name='parent_reference_identifier',
            new_name='parent_action_identifier',
        ),
        migrations.RenameField(
            model_name='protocoldeviationviolation',
            old_name='related_reference_identifier',
            new_name='related_action_identifier',
        ),
        migrations.RenameField(
            model_name='studyterminationconclusion',
            old_name='parent_reference_identifier',
            new_name='parent_action_identifier',
        ),
        migrations.RenameField(
            model_name='studyterminationconclusion',
            old_name='related_reference_identifier',
            new_name='related_action_identifier',
        ),
        migrations.RenameField(
            model_name='studyterminationconclusionw10',
            old_name='parent_reference_identifier',
            new_name='parent_action_identifier',
        ),
        migrations.RenameField(
            model_name='studyterminationconclusionw10',
            old_name='related_reference_identifier',
            new_name='related_action_identifier',
        ),
        migrations.AddField(
            model_name='deathreport',
            name='action_item',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.PROTECT, to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='deathreporttmg',
            name='action_item',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.PROTECT, to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='historicaldeathreport',
            name='action_item',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True,
                                    on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='historicaldeathreporttmg',
            name='action_item',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True,
                                    on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='historicalprotocoldeviationviolation',
            name='action_item',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True,
                                    on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='historicalstudyterminationconclusion',
            name='action_item',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True,
                                    on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='historicalstudyterminationconclusionw10',
            name='action_item',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True,
                                    on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='protocoldeviationviolation',
            name='action_item',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.PROTECT, to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='studyterminationconclusion',
            name='action_item',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.PROTECT, to='edc_action_item.ActionItem'),
        ),
        migrations.AddField(
            model_name='studyterminationconclusionw10',
            name='action_item',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.PROTECT, to='edc_action_item.ActionItem'),
        ),
        migrations.AlterField(
            model_name='deathreport',
            name='action_identifier',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='deathreporttmg',
            name='action_identifier',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='historicaldeathreport',
            name='action_identifier',
            field=models.CharField(null=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='historicaldeathreporttmg',
            name='action_identifier',
            field=models.CharField(null=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='historicalprotocoldeviationviolation',
            name='action_identifier',
            field=models.CharField(null=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='historicalstudyterminationconclusion',
            name='action_identifier',
            field=models.CharField(null=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='historicalstudyterminationconclusionw10',
            name='action_identifier',
            field=models.CharField(null=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='protocoldeviationviolation',
            name='action_identifier',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='studyterminationconclusion',
            name='action_identifier',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='studyterminationconclusionw10',
            name='action_identifier',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
