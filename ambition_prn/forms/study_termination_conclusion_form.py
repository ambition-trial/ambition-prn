from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_base.sites.forms import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..form_validators import StudyTerminationConclusionFormValidator
from ..models import StudyTerminationConclusion


class StudyTerminationConclusionForm(
    SiteModelFormMixin, FormValidatorMixin, ActionItemFormMixin, forms.ModelForm
):

    form_validator_cls = StudyTerminationConclusionFormValidator

    subject_identifier = forms.CharField(
        label="Subject Identifier",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    class Meta:
        model = StudyTerminationConclusion
        fields = "__all__"
        labels = {"offschedule_datetime": "Date patient terminated on study:"}
