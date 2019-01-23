from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_base.sites.forms import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import StudyTerminationConclusionW10
from ..form_validators import StudyTerminationConclusionW10FormValidator


class StudyTerminationConclusionW10Form(
    SiteModelFormMixin, FormValidatorMixin, ActionItemFormMixin, forms.ModelForm
):

    form_validator_cls = StudyTerminationConclusionW10FormValidator

    subject_identifier = forms.CharField(
        label="Subject Identifier",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    class Meta:
        model = StudyTerminationConclusionW10
        fields = "__all__"
        labels = {"offschedule_datetime": "Date patient terminated on study:"}
