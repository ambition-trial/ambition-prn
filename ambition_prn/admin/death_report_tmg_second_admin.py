from django.contrib import admin

from ..admin_site import ambition_prn_admin
from ..forms import DeathReportTmgForm
from ..models import DeathReportTmgSecond
from .death_report_tmg_admin import DeathReportTmgAdmin


@admin.register(DeathReportTmgSecond, site=ambition_prn_admin)
class DeathReportTmgSecondAdmin(DeathReportTmgAdmin):

    form = DeathReportTmgForm
