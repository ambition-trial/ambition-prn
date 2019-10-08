from django.db import models
from edc_adverse_event.constants import DEATH_REPORT_TMG_SECOND_ACTION
from edc_adverse_event.model_mixins import DeathReportTmgModelMixin
from edc_model.models import BaseUuidModel
from django.db.models.deletion import PROTECT
from edc_constants.constants import QUESTION_RETIRED, NOT_APPLICABLE
from ambition_prn.choices import TB_SITE_DEATH


class DeathReportTmg(DeathReportTmgModelMixin, BaseUuidModel):

    death_report = models.ForeignKey(f"ambition_prn.deathreport", on_delete=PROTECT)

    cause_of_death_old = models.CharField(
        verbose_name="Main cause of death",
        max_length=50,
        default=QUESTION_RETIRED,
        blank=True,
        null=True,
        help_text="Main cause of death in the opinion of TMG member",
    )

    tb_site = models.CharField(
        verbose_name="If cause of death is TB, specify site of TB disease",
        max_length=25,
        choices=TB_SITE_DEATH,
        default=NOT_APPLICABLE,
        blank=True,
    )

    class Meta(DeathReportTmgModelMixin.Meta):
        pass


class DeathReportTmgSecond(DeathReportTmg):

    action_name = DEATH_REPORT_TMG_SECOND_ACTION

    class Meta:
        proxy = True
