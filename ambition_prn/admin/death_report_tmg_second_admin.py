from django import forms
from django.contrib import admin
from edc_adverse_event.modeladmin_mixins import DeathReportTmgModelAdminMixin
from edc_model_admin.model_admin_simple_history import SimpleHistoryAdmin

from ..admin_site import ambition_prn_admin
from ..forms import DeathReportTmgSecondForm
from ..models import DeathReport, DeathReportTmgSecond


@admin.register(DeathReportTmgSecond, site=ambition_prn_admin)
class DeathReportTmgSecondAdmin(DeathReportTmgModelAdminMixin, SimpleHistoryAdmin):

    form = DeathReportTmgSecondForm

    @property
    def death_report_model_cls(self):
        return DeathReport
