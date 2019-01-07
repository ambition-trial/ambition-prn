from copy import copy
from django.contrib import admin
from edc_action_item import action_fieldset_tuple, action_fields
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import ambition_prn_admin
from ..forms import DeathReportForm
from ..models import DeathReport
from .modeladmin_mixins import ModelAdminMixin


@admin.register(DeathReport, site=ambition_prn_admin)
class DeathReportAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = DeathReportForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_identifier',
                'report_datetime',
                'death_datetime',
                'study_day',
                'death_as_inpatient')},
         ),
        ('Opinion of Local Study Doctor', {
            'fields': (
                'cause_of_death',
                'cause_of_death_other',
                'tb_site',
                'narrative')}),
        action_fieldset_tuple,
        audit_fieldset_tuple)

    radio_fields = {
        'death_as_inpatient': admin.VERTICAL,
        'cause_of_death': admin.VERTICAL,
        'tb_site': admin.VERTICAL}

    list_display = (
        'subject_identifier', 'dashboard', 'report_datetime',
        'cause_of_death', 'death_datetime', 'action_item', 'parent_action_item')

    list_filter = ('report_datetime', 'death_datetime', 'cause_of_death')

    search_fields = ['subject_identifier',
                     'action_identifier',
                     'tracking_identifier']

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        action_flds = copy(list(action_fields))
        action_flds.remove('action_identifier')
        fields = tuple(action_flds) + fields
        if obj:
            fields = fields + ('subject_identifier', )
        return fields
