from django.db import models
from edc_action_item.managers import ActionIdentifierSiteManager, ActionIdentifierManager
from edc_action_item.models import ActionModelMixin
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_base.model_validators import datetime_not_future
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO, NOT_APPLICABLE
from edc_identifier.model_mixins import TrackingModelMixin

from ..action_items import PROTOCOL_DEVIATION_VIOLATION_ACTION
from ..choices import PROTOCOL_VIOLATION, ACTION_REQUIRED, DEVIATION_VIOLATION, REPORT_STATUS


class ProtocolDeviationViolation(SiteModelMixin, ActionModelMixin,
                                 TrackingModelMixin, BaseUuidModel):

    action_name = PROTOCOL_DEVIATION_VIOLATION_ACTION

    tracking_identifier_prefix = 'PD'

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        default=get_utcnow)

    short_description = models.CharField(
        verbose_name='Provide a short description of this occurrence',
        max_length=35,
        null=True,
        blank=False,
        help_text=('Max 35 characters. Note: If this occurrence is a "violation" '
                   'there is additional space below for a more detailed '
                   'description'))

    report_type = models.CharField(
        verbose_name='Type of occurrence',
        max_length=25,
        choices=DEVIATION_VIOLATION)

    safety_impact = models.CharField(
        verbose_name='Could this occurrence have an impact on safety of the '
                     'participant?',
        max_length=25,
        choices=YES_NO)

    safety_impact_details = models.TextField(
        verbose_name='If "Yes", provide details',
        null=True,
        blank=True)

    study_outcomes_impact = models.CharField(
        verbose_name='Could this occurrence have an impact on study outcomes?',
        max_length=25,
        choices=YES_NO)

    study_outcomes_impact_details = models.TextField(
        verbose_name='If "Yes", provide details',
        null=True,
        blank=True)

    violation_datetime = models.DateTimeField(
        verbose_name='Date violation occurred',
        validators=[datetime_not_future],
        null=True,
        blank=True)

    violation_type = models.CharField(
        verbose_name='Type of violation',
        max_length=75,
        choices=PROTOCOL_VIOLATION,
        default=NOT_APPLICABLE)

    violation_type_other = models.CharField(
        null=True,
        blank=True,
        verbose_name='If other, please specify',
        max_length=75)

    violation_description = models.TextField(
        verbose_name='Describe the violation',
        null=True,
        blank=True,
        help_text=('Describe in full. Explain how the violation '
                   'happened, what occurred, etc.'))

    violation_reason = models.TextField(
        verbose_name='Explain the reason why the violation occurred',
        null=True,
        blank=True)

    corrective_action_datetime = models.DateTimeField(
        verbose_name='Corrective action date and time',
        validators=[datetime_not_future],
        null=True,
        blank=True)

    corrective_action = models.TextField(
        verbose_name='Corrective action taken',
        null=True,
        blank=True)

    preventative_action_datetime = models.DateTimeField(
        verbose_name='Preventative action date and time',
        validators=[datetime_not_future],
        null=True,
        blank=True)

    preventative_action = models.TextField(
        verbose_name='Preventative action taken',
        null=True,
        blank=True)

    action_required = models.CharField(
        max_length=45,
        choices=ACTION_REQUIRED)

    report_status = models.CharField(
        verbose_name='What is the status of this report?',
        max_length=25,
        choices=REPORT_STATUS)

    report_closed_datetime = models.DateTimeField(
        blank=True,
        null=True,
        validators=[datetime_not_future],
        verbose_name=('Date and time report closed.'))

    on_site = ActionIdentifierSiteManager()

    objects = ActionIdentifierManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.action_identifier, )

    class Meta:
        verbose_name = 'Protocol Deviation/Violation'
        verbose_name_plural = 'Protocol Deviations/Violations'
