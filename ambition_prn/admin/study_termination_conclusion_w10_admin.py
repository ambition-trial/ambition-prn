from django.contrib import admin
from edc_action_item import action_fieldset_tuple, action_fields
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import ambition_prn_admin
from ..forms import StudyTerminationConclusionW10Form
from ..models import StudyTerminationConclusionW10
from .modeladmin_mixins import ModelAdminMixin


@admin.register(StudyTerminationConclusionW10, site=ambition_prn_admin)
class StudyTerminationConclusionW10Admin(ModelAdminMixin, admin.ModelAdmin):

    form = StudyTerminationConclusionW10Form

    additional_instructions = (
        'Note: if the patient is deceased, complete the Death Report '
        'before completing this form. ')

    fieldsets = (
        [None, {
            'fields': (
                'subject_identifier',
                'offschedule_datetime',
                'last_study_fu_date',
                'termination_reason')}],
        action_fieldset_tuple,
        audit_fieldset_tuple
    )

    radio_fields = {'termination_reason': admin.VERTICAL}

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
