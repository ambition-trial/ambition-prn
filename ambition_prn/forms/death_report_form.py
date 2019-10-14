from django import forms
from edc_adverse_event.modelform_mixins import DeathReportModelFormMixin

from ..form_validators import DeathReportFormValidator
from ..models import DeathReport


class DeathReportForm(DeathReportModelFormMixin, forms.ModelForm):

    form_validator_cls = DeathReportFormValidator

    class Meta:
        model = DeathReport
        fields = "__all__"
