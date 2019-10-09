from ..models import DeathReportTmgSecond
from .death_report_tmg_form import DeathReportTmgForm


class DeathReportTmgSecondForm(DeathReportTmgForm):
    class Meta:
        model = DeathReportTmgSecond
        fields = "__all__"
