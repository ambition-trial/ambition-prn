from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_base.sites.forms import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..form_validators import ProtocolDeviationViolationFormValidator
from ..models import ProtocolDeviationViolation


class ProtocolDeviationViolationForm(
    SiteModelFormMixin, FormValidatorMixin, ActionItemFormMixin, forms.ModelForm
):

    form_validator_cls = ProtocolDeviationViolationFormValidator

    subject_identifier = forms.CharField(
        label="Subject Identifier",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    class Meta:
        model = ProtocolDeviationViolation
        fields = "__all__"
