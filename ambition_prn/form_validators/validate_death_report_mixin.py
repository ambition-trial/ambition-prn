from django import forms
from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from edc_base.utils import convert_php_dateformat
from edc_constants.constants import DEAD


class ValidateDeathReportMixin:

    death_report_model = 'ambition_prn.deathreport'

    @property
    def death_report_model_cls(self):
        return django_apps.get_model(self.death_report_model)

    def validate_death_report_if_deceased(self):
        """Validates death report exists of termination_reason
        is "DEAD.

        Note: uses __date field lookup. If using mysql don't forget
        to load timezone info.
        """
        subject_identifier = self.cleaned_data.get(
            'subject_identifier') or self.instance.subject_identifier

        try:
            death_report = self.death_report_model_cls.objects.get(
                subject_identifier=subject_identifier)
        except ObjectDoesNotExist:
            if self.cleaned_data.get('termination_reason') == DEAD:
                raise forms.ValidationError({
                    'termination_reason':
                    'Patient is deceased, please complete death report form first.'})
        else:
            if self.cleaned_data.get('death_date'):
                try:
                    self.death_report_model_cls.objects.get(
                        subject_identifier=subject_identifier,
                        death_datetime__date=self.cleaned_data.get('death_date'))
                except ObjectDoesNotExist:
                    expected = death_report.death_datetime.strftime(
                        convert_php_dateformat(settings.SHORT_DATE_FORMAT))
                    got = self.cleaned_data.get('death_date').strftime(
                        convert_php_dateformat(settings.SHORT_DATE_FORMAT))
                    raise forms.ValidationError({
                        'death_date':
                        'Date does not match Death Report. '
                        f'Expected {expected}. Got {got}.'})
