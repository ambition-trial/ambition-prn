from django.contrib import admin
from edc_model_admin import SimpleHistoryAdmin

from ..admin_site import ambition_prn_admin
from ..models import OnSchedule
from .modeladmin_mixins import ModelAdminMixin


@admin.register(OnSchedule, site=ambition_prn_admin)
class OnScheduleAdmin(ModelAdminMixin, SimpleHistoryAdmin):

    instructions = None
    fields = ("subject_identifier", "onschedule_datetime")

    list_display = ("subject_identifier", "dashboard", "onschedule_datetime")

    list_filter = ("onschedule_datetime",)

    def get_readonly_fields(self, request, obj=None):
        return ("subject_identifier", "onschedule_datetime")
