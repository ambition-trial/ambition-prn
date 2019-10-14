from django.contrib import admin
from edc_action_item import action_fieldset_tuple
from edc_adverse_event.modeladmin_mixins import DeathReportModelAdminMixin
from edc_model_admin import audit_fieldset_tuple, SimpleHistoryAdmin

from ..admin_site import ambition_prn_admin
from ..forms import DeathReportForm
from ..models import DeathReport


@admin.register(DeathReport, site=ambition_prn_admin)
class DeathReportAdmin(DeathReportModelAdminMixin, SimpleHistoryAdmin):

    form = DeathReportForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_identifier",
                    "report_datetime",
                    "death_datetime",
                    "study_day",
                    "death_as_inpatient",
                )
            },
        ),
        (
            "Opinion of Local Study Doctor",
            {
                "fields": (
                    "cause_of_death",
                    "cause_of_death_other",
                    "tb_site",
                    "narrative",
                )
            },
        ),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "death_as_inpatient": admin.VERTICAL,
        "cause_of_death": admin.VERTICAL,
        "tb_site": admin.VERTICAL,
    }
