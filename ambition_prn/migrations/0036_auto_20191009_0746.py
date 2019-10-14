# Generated by Django 2.2.6 on 2019-10-09 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ambition_prn", "0035_deathreporttmgsecond_historicaldeathreporttmgsecond")
    ]

    operations = [
        migrations.AlterModelOptions(
            name="deathreporttmgsecond",
            options={
                "verbose_name": "Death Report TMG",
                "verbose_name_plural": "Death Report TMG",
            },
        ),
        migrations.AlterModelOptions(
            name="historicaldeathreporttmgsecond",
            options={
                "get_latest_by": "history_date",
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Death Report TMG",
            },
        ),
    ]
