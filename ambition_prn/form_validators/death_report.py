from edc_adverse_event.form_validators import DeathReportFormValidator as FormValidator

from ..constants import TUBERCULOSIS
from .study_day_form_validator_mixin import StudyDayFormValidatorMixin


class DeathReportFormValidator(StudyDayFormValidatorMixin, FormValidator):
    def clean(self):

        super().clean()

        self.validate_study_day_with_datetime(
            study_day=self.cleaned_data.get("study_day"),
            compare_date=self.cleaned_data.get("death_datetime"),
            study_day_field="study_day",
        )

        tb = self.cause_of_death_model_cls.objects.get(short_name=TUBERCULOSIS)
        self.required_if(
            tb.short_name, field="cause_of_death", field_required="tb_site"
        )
