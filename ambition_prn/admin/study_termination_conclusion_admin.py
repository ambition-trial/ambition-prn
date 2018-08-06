from django.contrib import admin
from edc_action_item import action_fieldset_tuple, action_fields
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import ambition_prn_admin
from ..forms import StudyTerminationConclusionForm
from ..models import StudyTerminationConclusion
from .modeladmin_mixins import ModelAdminMixin


@admin.register(StudyTerminationConclusion, site=ambition_prn_admin)
class StudyTerminationConclusionAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = StudyTerminationConclusionForm

    additional_instructions = (
        'Note: if the patient is deceased, complete the Death Report '
        'before completing this form. ')

    fieldsets = (
        [None, {
            'fields': (
                'subject_identifier',
                'offschedule_datetime',
                'last_study_fu_date',
                'discharged_after_initial_admission',
                'initial_discharge_date',
                'readmission_after_initial_discharge',
                'readmission_date',
                'discharged_date',
                'termination_reason',
                'death_date',
                'consent_withdrawal_reason',
                'willing_to_complete_10w',
                'willing_to_complete_centre',
                'protocol_exclusion_criterion',
                'included_in_error',
                'included_in_error_date',
                'rifampicin_started',
                'first_line_regimen',
                'first_line_regimen_other',
                'first_line_choice',
                'second_line_regimen',
                'second_line_regimen_other',
                'arvs_switch_date',
                'arvs_delay_reason')}],
        action_fieldset_tuple,
        audit_fieldset_tuple
    )

    radio_fields = {
        'discharged_after_initial_admission': admin.VERTICAL,
        'readmission_after_initial_discharge': admin.VERTICAL,
        'termination_reason': admin.VERTICAL,
        'willing_to_complete_10w': admin.VERTICAL,
        'willing_to_complete_centre': admin.VERTICAL,
        'protocol_exclusion_criterion': admin.VERTICAL,
        'rifampicin_started': admin.VERTICAL,
        'first_line_regimen': admin.VERTICAL,
        'second_line_regimen': admin.VERTICAL,
        'first_line_choice': admin.VERTICAL}

    list_display = ('subject_identifier', 'dashboard',
                    'offschedule_datetime', 'last_study_fu_date',
                    'tracking_identifier', 'action_identifier')

    list_filter = ('offschedule_datetime', 'last_study_fu_date')

    search_fields = ('subject_identifier',
                     'action_identifier',
                     'tracking_identifier')

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        fields = action_fields + fields
        if obj:
            fields = fields + ('subject_identifier', )
        return fields
