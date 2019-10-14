from django.contrib import admin
from edc_adverse_event.modeladmin_mixins import DeathReportTmgModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin

from ..admin_site import ambition_prn_admin
from ..forms import DeathReportTmgForm
from ..models import DeathReport, DeathReportTmg


@admin.register(DeathReportTmg, site=ambition_prn_admin)
class DeathReportTmgAdmin(DeathReportTmgModelAdminMixin, SimpleHistoryAdmin):

    form = DeathReportTmgForm

    @property
    def death_report_model_cls(self):
        return DeathReport
